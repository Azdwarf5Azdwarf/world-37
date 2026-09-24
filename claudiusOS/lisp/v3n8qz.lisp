;;;; mini-lisp-os.lisp
;;;; A self-hosting reflective Lisp OS prototype.
;;;; Load with: sbcl --load mini-lisp-os.lisp
;;;; Then run: (boot-os)

;; ============================================================
;; 0. UTILITIES
;; ============================================================

(defpackage :mini-lisp-os
  (:use :cl)
  (:shadow #:pairlis)
  (:export :boot-os :eval-in :source-of :redefine :spawn-agent
           :ps :kill-agent :traverse-up))

(in-package :mini-lisp-os)

(defvar *process-table* '()
  "List of (pid name closure state); state is :ready, :running, :waiting.")

(defvar *next-pid* 0)

(defun pairlis (keys vals &optional (alist '()))
  "Build an association list from keys and values."
  (append (mapcar #'cons keys vals) alist))

(defun assq (key alist)
  "Association list lookup."
  (assoc key alist :test #'eq))

;; ============================================================
;; 1. THE METACIRCULAR EVALUATOR (The Substrate)
;; ============================================================
;; This is the heart. A Lisp interpreter written in Lisp.
;; Because it is just lists, the OS can inspect and modify it.

(defvar *os-global-env* '()
  "The root environment of the OS. A list of (symbol . value) pairs.")

(defvar *os-source-registry* (make-hash-table :test #'eq)
  "Maps function names to their source S-expressions.
   This is the 'traversal' mechanism: code can read code.")

(defun register-source (name expr)
  (setf (gethash name *os-source-registry*) expr))

(defun lookup (sym env)
  "Look up a symbol in the local environment, then global."
  (let ((local (cdr (assq sym env))))
    (if local
        local
        (cdr (assq sym *os-global-env*)))))

;; --- The Evaluator ---

(defun os-eval (expr env)
  "Metacircular evaluator. Evaluates EXPR in ENV."
  (cond
    ;; Self-evaluating
    ((or (numberp expr) (stringp expr) (characterp expr) (null expr)) expr)
    
    ;; Quote
    ((and (consp expr) (eq (car expr) 'quote))
     (cadr expr))
    
    ;; Variable reference
    ((symbolp expr)
     (lookup expr env))
    
    ;; Definition (global)
    ((and (consp expr) (eq (car expr) 'def))
     (let ((name (cadr expr))
           (params (caddr expr))
           (body (cdddr expr)))
       (let ((closure (make-closure params body env)))
         (setf *os-global-env* (cons (cons name closure) *os-global-env*))
         (register-source name expr)
         name)))
    
    ;; Lambda (anonymous function)
    ((and (consp expr) (eq (car expr) 'lambda))
     (make-closure (cadr expr) (cddr expr) env))
    
    ;; If
    ((and (consp expr) (eq (car expr) 'if))
     (if (os-eval (cadr expr) env)
         (os-eval (caddr expr) env)
         (os-eval (cadddr expr) env)))
    
    ;; Set! (mutation)
    ((and (consp expr) (eq (car expr) 'set!))
     (let ((val (os-eval (caddr expr) env)))
       (set-binding! (cadr expr) val env)
       val))
    
    ;; Begin (sequence)
    ((and (consp expr) (eq (car expr) 'begin))
     (eval-sequence (cdr expr) env))
    
    ;; Let
    ((and (consp expr) (eq (car expr) 'let))
     (let ((bindings (cadr expr))
           (body (cddr expr)))
       (let ((new-env (pairlis (mapcar #'car bindings)
                               (mapcar (lambda (b) (os-eval (cadr b) env)) bindings)
                               env)))
         (eval-sequence body new-env))))
    
    ;; Application
    ((consp expr)
     (os-apply (os-eval (car expr) env)
               (mapcar (lambda (e) (os-eval e env)) (cdr expr))))
    
    (t (error "Unknown expression: ~a" expr))))

(defun eval-sequence (exprs env)
  (if (null (cdr exprs))
      (os-eval (car exprs) env)
      (progn (os-eval (car exprs) env)
             (eval-sequence (cdr exprs) env))))

(defun make-closure (params body env)
  "A closure is a list: (closure params body env)"
  (list 'closure params body env))

(defun closure-p (obj)
  (and (consp obj) (eq (car obj) 'closure)))

(defun closure-params (c) (cadr c))
(defun closure-body   (c) (caddr c))
(defun closure-env    (c) (cadddr c))

(defun os-apply (proc args)
  "Apply a closure or primitive to arguments."
  (cond
    ((closure-p proc)
     (eval-sequence (closure-body proc)
                    (pairlis (closure-params proc) args (closure-env proc))))
    
    ((functionp proc)
     (apply proc args))
    
    (t (error "Not a procedure: ~a" proc))))

(defun set-binding! (sym val env)
  "Destructively update a binding."
  (let ((pair (assq sym env)))
    (if pair
        (rplacd pair val)
        (let ((global (assq sym *os-global-env*)))
          (if global
              (rplacd global val)
              (setf *os-global-env* (cons (cons sym val) *os-global-env*)))))))

;; ============================================================
;; 2. REFLECTION PRIMITIVES (The Traversal Mechanism)
;; ============================================================
;; These let the system inspect and rewrite its own definitions.

(defun source-of (name)
  "Return the source S-expression of a defined function.
   This is 'traversing into upper code'—reading the layer above."
  (gethash name *os-source-registry*))

(defun redefine (name new-source-expr)
  "Replace a function's definition at runtime.
   The OS can rewrite itself."
  (let ((parsed (if (and (consp new-source-expr)
                         (eq (car new-source-expr) 'def))
                    new-source-expr
                    (list 'def name '() new-source-expr))))
    (os-eval parsed '())
    (register-source name parsed)
    name))

(defun traverse-up (name)
  "Print the source of a function and its dependencies."
  (let ((src (source-of name)))
    (format t "~%=== SOURCE OF ~a ===~%~s~%" name src)
    (when (consp src)
      (let ((deps (remove-if-not #'symbolp (flatten (cddr src)))))
        (format t "~%Dependencies: ~a~%" deps)
        (dolist (d deps)
          (when (gethash d *os-source-registry*)
            (format t "  ~a -> defined in OS~%" d)))))
    src))

(defun flatten (tree)
  "Flatten a nested list."
  (cond ((null tree) nil)
        ((atom tree) (list tree))
        (t (append (flatten (car tree)) (flatten (cdr tree))))))

;; ============================================================
;; 3. PRIMITIVE OPERATIONS (The 'Syscalls')
;; ============================================================
;; These are the bridge between the metacircular world and CL.

(defun install-primitives ()
  "Bind primitive operations into the global OS environment."
  (setf *os-global-env*
        (list
         (cons '+ #'+)
         (cons '- #'-)
         (cons '* #'*)
         (cons '/ #'/)
         (cons '> #'>)
         (cons '< #'<)
         (cons '= #'=)
         (cons 'cons #'cons)
         (cons 'car #'car)
         (cons 'cdr #'cdr)
         (cons 'list #'list)
         (cons 'null #'null)
         (cons 'eq #'eq)
         (cons 'print (lambda (x) (format t "~%~s~%" x) x))
         (cons 'self
               (lambda ()
                 (format t "~%=== OS SELF-INSPECTION ===~%")
                 (format t "Global bindings: ~a~%"
                         (mapcar #'car *os-global-env*))
                 (format t "Registered sources: ~a~%"
                         (loop for k being the hash-keys of *os-source-registry*
                               collect k))
                 t))
         (cons 'ps
               (lambda ()
                 (format t "~%=== PROCESS TABLE ===~%")
                 (dolist (p *process-table*)
                   (format t "[~a] state=~a~%" (car p) (fourth p)))
                 t)))))

;; ============================================================
;; 4. THE OS KERNEL (Processes & Scheduler)
;; ============================================================
;; Processes are agents with their own code, environment, and state.

(defun spawn-agent (name source-expr &optional (parent-env '()))
  "Create a new agent from source code. Returns PID."
  (let ((pid (incf *next-pid*)))
    (let ((closure (os-eval source-expr parent-env)))
      (push (list pid name closure :ready) *process-table*)
      pid)))

(defun ps ()
  "List all agents."
  (format t "~%PID  NAME           STATE~%")
  (format t "---  ----           -----~%")
  (dolist (p *process-table*)
    (format t "~3a  ~14a ~a~%" (car p) (cadr p) (fourth p))))

(defun kill-agent (pid)
  (setf *process-table* (remove-if (lambda (p) (= (car p) pid)) *process-table*)))

(defun run-agent (pid)
  "Execute one 'quantum' of an agent."
  (let ((proc (find-if (lambda (p) (= (car p) pid)) *process-table*)))
    (when proc
      (setf (fourth proc) :running)
      (let ((result (os-apply (third proc) '())))
        (setf (fourth proc) :ready)
        result))))

(defun scheduler-tick ()
  "Round-robin: run the next ready agent."
  (let ((ready (find-if (lambda (p) (eq (fourth p) :ready)) *process-table*)))
    (when ready
      (run-agent (car ready)))))

;; ============================================================
;; 5. THE BOOT SEQUENCE
;; ============================================================

(defun boot-os ()
  "Initialize and demonstrate the mini Lisp OS."
  (format t "~%========================================")
  (format t "~%   MINI LISP OS - REFLECTIVE KERNEL")
  (format t "~%========================================~%")
  
  ;; 0. Install primitives
  (install-primitives)
  (format t "~%[BOOT] Primitives installed.~%")
  
  ;; 1. Define some OS-level functions in the metacircular evaluator
  (os-eval '(def square (x) (* x x)) '())
  (os-eval '(def factorial (n)
              (if (= n 0)
                  1
                  (* n (factorial (- n 1)))))
           '())
  (os-eval '(def fib (n)
              (if (< n 2)
                  n
                  (+ (fib (- n 1)) (fib (- n 2)))))
           '())
  
  (format t "[BOOT] Metacircular functions defined.~%")
  
  ;; 2. Demonstrate normal evaluation
  (format t "~%[DEMO] Evaluating (factorial 5): ~a"
          (os-eval '(factorial 5) '()))
  (format t "~%[DEMO] Evaluating (square 12): ~a"
          (os-eval '(square 12) '()))
  
  ;; 3. DEMONSTRATE REFLECTION (Traversing into upper code)
  (format t "~%~%[REFLECTION] Inspecting source of 'factorial':")
  (traverse-up 'factorial)
  
  ;; 4. DEMONSTRATE SELF-MODIFICATION
  (format t "~%~%[SELF-MOD] Redefining 'square' to cube:")
  (redefine 'square '(def square (x) (* x (* x x))))
  (format t "Evaluating new (square 3): ~a"
          (os-eval '(square 3) '()))
  
  ;; 5. Spawn agents
  (format t "~%~%[AGENTS] Spawning computational agents...~%")
  (spawn-agent 'counter
               '(lambda () (begin (print 'agent-running)
                                  (self))))
  (spawn-agent 'math-bot
               '(lambda () (begin (print (factorial 4))
                                  (print (fib 10)))))
  
  (ps)
  
  ;; 6. Run scheduler
  (format t "~%~%[KERNEL] Running scheduler tick...~%")
  (scheduler-tick)
  (scheduler-tick)
  
  ;; 7. Final introspection
  (format t "~%~%[FINAL] Full OS state:~%")
  (os-eval '(self) '())
  
  (format t "~%~%========================================")
  (format t "~%   OS BOOT COMPLETE")
  (format t "~%   Type (boot-os) to restart.")
  (format t "~%   Type (traverse-up 'name) to inspect code.")
  (format t "~%   Type (ps) to see agents.")
  (format t "~%========================================~%")
  
  'os-ready)

;; Auto-boot if loaded directly
(boot-os)
