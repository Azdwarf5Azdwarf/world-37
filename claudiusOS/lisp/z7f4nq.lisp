;;;; Titel: Lisp -> tensor-IR -> PyTorch. Kompilatorlager, single-file.
;;;; Hör ihop med: features/y8g9e5.md, steg 1-2 och 5 i liten skala.
;;;; Kör: sbcl --non-interactive --load z7f4nq.lisp
;;;; Genererar build/*.py och kör en självtest-svit sist.
;;;;
;;;; Modellen skrivs i Lisp. Frontend lågnivåfierar (lowers) formerna till
;;;; en tensor-IR (mellanrepresentation) där varje nod har känd in- och
;;;; utdimension. Backend är ett rent pass över IR:n; PyTorch är bara ett
;;;; av flera tänkbara mål.

(defpackage :nn-compile
  (:use :cl)
  (:export #:defmodel #:model-ir #:emit-pytorch #:emit-file))

(in-package :nn-compile)

;; === 1. Register och hjälpare ===

(defvar *models* (make-hash-table :test 'equal)
  "Modellnamn (gemener, sträng) -> plist med :ir, :in och :out.")

(defvar *attr-counter* nil "Prefix -> löpnummer, för läsbara attributnamn.")
(defvar *init-lines* '() "Rader till __init__, omvänd ordning.")
(defvar *fwd-lines* '() "Rader till forward, omvänd ordning.")

(defun op-name (form)
  (unless (and (consp form) (symbolp (first form)))
    (error "varje form måste vara (operation ...), fick: ~s" form))
  (string-downcase (symbol-name (first form))))

(defun as-keyword (name)
  (intern (string-upcase name) :keyword))

(defun next-attr (prefix)
  "Numrera per prefix: fc1, fc2, attn1 ... i stället för en gemensam räknare."
  (format nil "~a~d" prefix (incf (gethash prefix *attr-counter* 0))))

;; === 2. Frontend: DSL -> tensor-IR ===
;;
;; En IR-nod är en plist: (:op :linear :in 784 :out 128).
;; Dimensionen bärs framåt genom listan, så (linear 128) räcker att skriva
;; — indimensionen härleds. Det är hela poängen med IR-steget: felaktiga
;; former fastnar här, inte i Python vid första framåtpasset.

(defparameter +activations+ '("relu" "gelu" "tanh" "sigmoid" "softmax"))

(defun lower (forms &optional dim)
  "Lågnivåfiera FORMS. DIM är indimensionen in i blocket.
Returnerar (values ir ut-dimension)."
  (let ((ir '()))
    (dolist (form forms)
      (let ((op (op-name form))
            (args (rest form)))
        (flet ((need-dim ()
                 (or dim (error "~a: indimensionen är okänd — sätt (input n) först" op))))
          (cond
            ((string= op "input")
             (setf dim (first args)))

            ((string= op "linear")
             (need-dim)
             (push (list :op :linear :in dim :out (first args)) ir)
             (setf dim (first args)))

            ((string= op "embedding")
             (push (list :op :embedding :vocab (first args) :in (first args)
                         :out (second args))
                   ir)
             (setf dim (second args)))

            ((string= op "attention")
             (need-dim)
             (let ((heads (or (getf args :heads) 8)))
               (unless (zerop (mod dim heads))
                 (error "attention: dimensionen ~d är inte jämnt delbar med ~d huvuden"
                        dim heads))
               (push (list :op :attention :in dim :out dim :heads heads) ir)))

            ((string= op "layernorm")
             (need-dim)
             (push (list :op :layernorm :in dim :out dim) ir))

            ((string= op "dropout")
             (need-dim)
             (push (list :op :dropout :in dim :out dim :p (or (first args) 0.1)) ir))

            ((member op +activations+ :test #'string=)
             (need-dim)
             (push (list :op (as-keyword op) :in dim :out dim) ir))

            ((string= op "residual")
             (need-dim)
             (multiple-value-bind (body out) (lower args dim)
               (unless (eql out dim)
                 (error "residual: blocket ändrar dimension ~d -> ~d, summan går inte ihop"
                        dim out))
               (push (list :op :residual :in dim :out dim :body body) ir)))

            ((string= op "repeat")
             (let ((n (first args)))
               (unless (and (integerp n) (plusp n))
                 (error "repeat: antalet måste vara ett positivt heltal, fick ~s" n))
               (dotimes (i n)
                 (multiple-value-bind (body out) (lower (rest args) dim)
                   (setf ir (append (reverse body) ir)
                         dim out)))))

            (t (error "okänd operation: ~a" (first form)))))))
    (values (nreverse ir) dim)))

;; === 3. Backend: tensor-IR -> PyTorch ===
;;
;; Två listor byggs parallellt: modulerna i __init__ och satserna i forward.
;; Aktiveringar blir funktionsanrop (inget tillstånd), lager blir moduler.

(defun emit-node (node var)
  (let ((op (getf node :op))
        (in (getf node :in))
        (out (getf node :out)))
    (flet ((module (prefix ctor call)
             (let ((attr (next-attr prefix)))
               (push (format nil "self.~a = ~a" attr ctor) *init-lines*)
               (push (format nil call attr) *fwd-lines*)))
           (call (fmt &rest args)
             (push (apply #'format nil fmt args) *fwd-lines*)))
      (ecase op
        (:linear
         (module "fc" (format nil "torch.nn.Linear(~d, ~d)" in out)
                 (format nil "~a = self.~~a(~a)" var var)))
        (:embedding
         (module "emb" (format nil "torch.nn.Embedding(~d, ~d)" (getf node :vocab) out)
                 (format nil "~a = self.~~a(~a)" var var)))
        (:layernorm
         (module "norm" (format nil "torch.nn.LayerNorm(~d)" in)
                 (format nil "~a = self.~~a(~a)" var var)))
        (:dropout
         (module "drop" (format nil "torch.nn.Dropout(~a)" (getf node :p))
                 (format nil "~a = self.~~a(~a)" var var)))
        (:attention
         (module "attn"
                 (format nil "torch.nn.MultiheadAttention(~d, ~d, batch_first=True)"
                         in (getf node :heads))
                 (format nil "~a, _ = self.~~a(~a, ~a, ~a)" var var var var)))
        (:relu    (call "~a = torch.nn.functional.relu(~a)" var var))
        (:gelu    (call "~a = torch.nn.functional.gelu(~a)" var var))
        (:tanh    (call "~a = torch.tanh(~a)" var var))
        (:sigmoid (call "~a = torch.sigmoid(~a)" var var))
        (:softmax (call "~a = torch.nn.functional.softmax(~a, dim=-1)" var var))
        (:residual
         (let ((saved (next-attr "res")))
           (call "~a = ~a" saved var)
           (dolist (child (getf node :body))
             (emit-node child var))
           (call "~a = ~a + ~a" var var saved)))))))

(defun py-class-name (name)
  "tiny-net -> TinyNet"
  (let ((s (string-downcase name))
        (parts '())
        (start 0))
    (loop for pos = (position #\- s :start start)
          do (push (subseq s start pos) parts)
             (unless pos (return))
             (setf start (1+ pos)))
    (format nil "~{~:(~a~)~}" (nreverse parts))))

(defun emit-pytorch (name &optional (stream *standard-output*))
  "Skriv modellen NAME som PyTorch-källkod till STREAM."
  (let* ((entry (or (gethash (string-downcase name) *models*)
                    (error "okänd modell: ~a" name)))
         (ir (getf entry :ir))
         (*attr-counter* (make-hash-table :test 'equal))
         (*init-lines* '())
         (*fwd-lines* '()))
    (dolist (node ir)
      (emit-node node "x"))
    (format stream "# Genererad från Lisp av z7f4nq.lisp. Ändra inte för hand.~%")
    (format stream "# in=~d ut=~d noder=~d~%import torch~%~%~%"
            (getf entry :in) (getf entry :out) (length ir))
    (format stream "class ~a(torch.nn.Module):~%" (py-class-name name))
    (format stream "    def __init__(self):~%        super().__init__()~%")
    (format stream "~{        ~a~%~}~%" (reverse *init-lines*))
    (format stream "    def forward(self, x):~%")
    (format stream "~{        ~a~%~}" (reverse *fwd-lines*))
    (format stream "        return x~%")
    name))

(defun emit-file (name path)
  (ensure-directories-exist path)
  (with-open-file (out path :direction :output :if-exists :supersede
                            :if-does-not-exist :create)
    (emit-pytorch name out))
  path)

;; === 4. DSL-makrot ===

(defmacro defmodel (name &body forms)
  "Definiera en modell. Formerna typas vid definitionen, inte vid körning."
  (let ((key (string-downcase (symbol-name name))))
    `(multiple-value-bind (ir out) (lower ',forms)
       (setf (gethash ,key *models*)
             (list :ir ir :in (getf (first ir) :in) :out out))
       ',name)))

(defun model-ir (name)
  (getf (gethash (string-downcase name) *models*) :ir))

;; === 5. Modeller ===

(defmodel tiny-net
  (input 784)
  (linear 128)
  (relu)
  (linear 10))

(defmodel mythos-small
  (input 512)
  (repeat 3
    (residual
      (layernorm)
      (attention :heads 8)
      (dropout 0.1))
    (residual
      (layernorm)
      (linear 2048)
      (gelu)
      (linear 512)))
  (layernorm)
  (linear 32000))

;; === 6. Självtest ===

(defvar *fails* 0)

(defun check (label ok)
  (format t "~:[FAIL~;ok  ~]  ~a~%" ok label)
  (unless ok (incf *fails*)))

(defmacro check-error (label &body body)
  `(check ,label (handler-case (progn ,@body nil) (error () t))))

(defun py (name) (with-output-to-string (s) (emit-pytorch name s)))

(defun count-substring (needle haystack)
  (loop with n = 0 with start = 0
        for pos = (search needle haystack :start2 start)
        while pos do (incf n) (setf start (+ pos (length needle)))
        finally (return n)))

(let ((tiny (py "tiny-net"))
      (mythos (py "mythos-small")))
  (check "tiny-net: klassnamn"      (search "class TinyNet(torch.nn.Module):" tiny))
  (check "tiny-net: härledd form"   (search "torch.nn.Linear(784, 128)" tiny))
  (check "tiny-net: andra lagret"   (search "torch.nn.Linear(128, 10)" tiny))
  (check "tiny-net: forward stänger" (search "return x" tiny))
  (check "mythos: attention"        (search "MultiheadAttention(512, 8, batch_first=True)" mythos))
  (check "mythos: tuppel-uppackning" (search "x, _ = self.attn1(x, x, x)" mythos))
  (check "mythos: residual adderar" (search "x = x + res" mythos))
  (check "mythos: repeat vecklas ut, 3 block"
         (= 3 (count-substring "MultiheadAttention" mythos)))
  (check "mythos: utdimension"      (search "torch.nn.Linear(512, 32000)" mythos)))

(check-error "linear före input avvisas" (lower '((linear 128))))
(check-error "okänd operation avvisas"   (lower '((input 8) (konvolution 3))))
(check-error "attention med ojämna huvuden avvisas"
  (lower '((input 100) (attention :heads 8))))
(check-error "residual som ändrar dimension avvisas"
  (lower '((input 512) (residual (linear 256)))))
(check-error "repeat med skräpantal avvisas"
  (lower '((input 8) (repeat -1 (linear 8)))))
(check-error "okänd modell avvisas" (py "finns-inte"))

(emit-file "tiny-net" "build/tiny_net.py")
(emit-file "mythos-small" "build/mythos_small.py")

(format t "~%build/tiny_net.py och build/mythos_small.py skrivna.~%")
(if (zerop *fails*)
    (format t "TRANSPILE OK~%")
    (progn (format t "~d TEST FALLERADE~%" *fails*)
           #+sbcl (sb-ext:exit :code 1)))
