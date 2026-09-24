;;;; t8k2vr — testsvit för Lisp-spåret i claudiusOS
;;;; Kör: sbcl --non-interactive --load t8k2vr.lisp
;;;;
;;;; Ordningen är Mezzanos: först bootar systemet, sedan testas det som
;;;; bootade. Ett OS som inte bootar behöver inga enhetstester än.
;;;;
;;;; Idiomet (check / check-error / *fails*) är kopierat från z7f4nq.lisp §6
;;;; med flit — inget testbibliotek, inga beroenden utanför ANSI CL.

;; === 0. Testramen ===

(defvar *fails* 0)

(defun check (label ok)
  (format t "~:[FAIL~;ok  ~]  ~a~%" ok label)
  (unless ok (incf *fails*)))

(defmacro check-error (label &body body)
  `(check ,label (handler-case (progn ,@body nil) (error () t))))

(defmacro quietly (&body body)
  "Kör BODY utan att dess utskrifter smutsar ner testloggen."
  `(let ((*standard-output* (make-broadcast-stream))) ,@body))

(defvar *here* (or *load-truename* *default-pathname-defaults*))
(defun sibling (name) (merge-pathnames name *here*))

;; === 1. Boot-testet: v3n8qz.lisp ===
;;
;; Filen auto-bootar när den laddas. Fånga utskriften och assertera på den,
;; så blir regeln i AGENTS.md kod i stället för något någon tittar på.

(defvar *boot-errors* nil)

(defvar *boot-output*
  (with-output-to-string (out)
    (setf *boot-errors*
          (with-output-to-string (err)
            (let ((*standard-output* out) (*error-output* err))
              (load (sibling "v3n8qz.lisp")))))))

(format t "~%--- v3n8qz.lisp: boot ---~%")
(check "bootar hela vägen"        (search "OS BOOT COMPLETE" *boot-output*))
(check "primitiver installerade"  (search "[BOOT] Primitives installed." *boot-output*))
(check "reflektionen kördes"      (search "[REFLECTION]" *boot-output*))
(check "självmodifiering gav 27"  (search "(square 3): 27" *boot-output*))
(check "processtabellen visades"  (search "[AGENTS]" *boot-output*))
(check "ingen backtrace"          (not (search "Backtrace" *boot-output*)))
(check "inga riktiga varningar"   (not (search "caught WARNING" *boot-errors*)))

;; === 2. Evaluatorn ===
;;
;; OS:et har sin egen namnrymd: `factorial`, `def` och `self` är symboler i
;; paketet :mini-lisp-os, inte i CL-USER. Läs därför uttrycken i OS:ets
;; paket — annars slår `assq` (som jämför med `eq`) aldrig till.

(defun os-read (string)
  (let ((*package* (find-package :mini-lisp-os)))
    (read-from-string string)))

(defun os (string)
  "Evaluera STRING i OS:ets globala miljö."
  (mini-lisp-os::os-eval (os-read string) '()))

(format t "~%--- v3n8qz.lisp: metacirkulär evaluator ---~%")
(check "självevaluerande tal"    (eql 42 (os "42")))
(check "självevaluerande sträng" (string= "hej" (os "\"hej\"")))
(check "quote"           (eq (os-read "hej") (os "'hej")))
(check "if väljer then"  (eq (os-read "ja")  (os "(if (= 1 1) 'ja 'nej)")))
(check "if väljer else"  (eq (os-read "nej") (os "(if (= 1 2) 'ja 'nej)")))
(check "lambda + applikation" (eql 42 (os "((lambda (x) (* x 2)) 21)")))
(check "let binder lokalt"    (eql 9  (os "(let ((x 3)) (* x x))")))
(check "begin returnerar sista värdet" (eql 2 (os "(begin 1 2)")))
(check "rekursion: (factorial 5)" (eql 120 (os "(factorial 5)")))
(check "rekursion: (fib 10)"      (eql 55  (os "(fib 10)")))
(check "def returnerar namnet"
       (eq (os-read "dubbel") (os "(def dubbel (x) (* x 2))")))
(check "definierad funktion räknar rätt" (eql 8 (os "(dubbel 4)")))
(check "set! muterar global bindning"
       (progn (os "(def teller 1)") (os "(set! teller 5)") (eql 5 (os "teller"))))
(check-error "okänt uttryck avvisas" (mini-lisp-os::os-eval #(1 2) '()))
(check-error "icke-procedur går inte att applicera" (mini-lisp-os::os-apply 7 '()))

;; === 3. Vertikal traversering (reflektion) ===
;;
;; README:s arkitekturavsnitt lovar (source-of 'f) och (redefine 'f ...).
;; Det här är testet som håller det löftet.

(format t "~%--- v3n8qz.lisp: vertikal traversering ---~%")
(check "source-of ger källan som lista"
       (let ((src (mini-lisp-os:source-of (os-read "factorial"))))
         (and (consp src)
              (eq (car src) (os-read "def"))
              (eq (cadr src) (os-read "factorial")))))
(check "source-of på okänt namn ger nil"
       (null (mini-lisp-os:source-of (os-read "finns-inte"))))
(check "redefine byter definition i drift"
       (progn (mini-lisp-os:redefine (os-read "dubbel")
                                     (os-read "(def dubbel (x) (* x 3))"))
              (eql 12 (os "(dubbel 4)"))))
(check "registret följer med redefine"
       (equal (os-read "(def dubbel (x) (* x 3))")
              (mini-lisp-os:source-of (os-read "dubbel"))))
(check "traverse-up skriver ut källan"
       (search "SOURCE OF FACTORIAL"
               (with-output-to-string (s)
                 (let ((*standard-output* s))
                   (mini-lisp-os:traverse-up (os-read "factorial"))))))

;; === 4. Processtabellen och schemaläggaren ===
;;
;; Posten är (pid name closure state) — fyra fält, state är fourth.

(format t "~%--- v3n8qz.lisp: processtabell ---~%")
(defvar *before* (length mini-lisp-os::*process-table*))
(defvar *pid* (quietly (mini-lisp-os:spawn-agent 'test-agent (os-read "(lambda () 7)"))))

(check "spawn-agent ger ett pid" (and (integerp *pid*) (> *pid* 0)))
(check "tabellen växte med en"
       (= (1+ *before*) (length mini-lisp-os::*process-table*)))

(defvar *entry* (find *pid* mini-lisp-os::*process-table* :key #'first))
(check "posten har fyra fält"      (= 4 (length *entry*)))
(check "andra fältet är namnet"    (eq 'test-agent (second *entry*)))
(check "tredje fältet är closuren" (mini-lisp-os::closure-p (third *entry*)))
(check "fjärde fältet är :ready"   (eq :ready (fourth *entry*)))
(check "run-agent kör closuren"    (eql 7 (quietly (mini-lisp-os::run-agent *pid*))))
(check "agenten är :ready igen"    (eq :ready (fourth *entry*)))
(check "scheduler-tick tar den första :ready"
       (eql 7 (quietly (mini-lisp-os::scheduler-tick))))
(check "ps listar agenten"
       (search "TEST-AGENT" (with-output-to-string (s)
                              (let ((*standard-output* s)) (mini-lisp-os:ps)))))
(check "kill-agent tar bort posten"
       (progn (mini-lisp-os:kill-agent *pid*)
              (and (= *before* (length mini-lisp-os::*process-table*))
                   (null (find *pid* mini-lisp-os::*process-table* :key #'first)))))

;; === 5. k9x2m4.lisp — symboliskt tidsspråk ===
;;
;; Bara det som faktiskt står i features/q3w8n1.md testas. Att färgen
;; härleds ur tempus är öppen fråga Q2 — den låses inte fast här.

(load (sibling "k9x2m4.lisp"))

(format t "~%--- k9x2m4.lisp: bas 57 ---~%")
(check "3 x 19 = 57"            (= 57 (* +lines+ +tier+)))
(check "(base57 43) -> (2 5)"   (equal '(2 5) (base57 43)))
(check "rundgång: 2*19+5 = 43"
       (let ((r (base57 43))) (= 43 (+ (* +tier+ (first r)) (second r)))))
(check "under en ruta: (base57 5) -> (0 5)" (equal '(0 5) (base57 5)))
(check "jämnt: (base57 57) -> (3 0)"        (equal '(3 0) (base57 57)))
(check-error "negativt tal avvisas" (base57 -1))
(check-error "icke-heltal avvisas"  (base57 1.5))

(format t "~%--- k9x2m4.lisp: kvadreringen ---~%")
(check "nuet kvadreras aldrig"  (eq :none (choose-color :present)))
(check "nuet lämnar rutan tom"  (eq :none (when-time :present *square*)))
(check "dåtid ger en färg ur *color*"   (when-time :past   (member *square* *color*)))
(check "framtid ger en färg ur *color*" (when-time :future (member *square* *color*)))
(check "*square* återställs efter when-time"
       (progn (when-time :future *square*) (eq :none *square*)))
(check-error "okänt tempus avvisas" (choose-color :imorgon))

;; === 6. Utfall ===

(format t "~%")
(if (zerop *fails*)
    (format t "LISP-TESTER OK~%")
    (progn (format t "~d TEST FALLERADE~%" *fails*)
           #+sbcl (sb-ext:exit :code 1)))
