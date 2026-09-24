;;;; k9x2m4 — symboliskt tidsspråk, skiss (2026-08-29)
;;;; Bas 57 = 3 x 19. Nuet = tre linjer. Tid nämns -> triangeln kvadreras -> färg.
;;;; Kör: sbcl --non-interactive --load k9x2m4.lisp
;;;; Bakgrund: features/k9x2m4.md (rå diktering), features/q3w8n1.md (manifest).

;; --- Specialvariabler överst, före all användning ---

(defparameter *color* '(:red :blue :green)
  "Svaren som rutan kräver: ja / nej-kanske / ovisshet.")

(defvar *square* :none
  "Färgen på den kvadrerade triangeln. :none = vi står kvar i nuet.")

(defconstant +lines+ 3   "Nuet: de tre linjerna som håller verkligheten.")
(defconstant +tier+  19  "Volymen i varje ruta. Manifestet §V.")

;; Tre linjer = nuet (present är alltid 3)
(defstruct triad a b c)                        ; 3D-verkligheten, 90-graders triangeln

;; Bas 57 = 3 x 19
(defun base57 (n)
  "Dela N i 19-block. -> (kvot rest). 43 ger (2 5): två fulla rutor och fem över."
  (unless (and (integerp n) (>= n 0))
    (error "base57 vill ha ett icke-negativt heltal, fick: ~s" n))
  (multiple-value-list (floor n +tier+)))

(defun choose-color (tense)
  "Vilket svar rutan kräver. :present kvadreras aldrig."
  (let ((c (case tense
             (:present :none)      ; nuet: kvar i de tre linjerna, ingen kvadrering
             (:past    :green)     ; ovisshet
             (:future  :blue)      ; nej/kanske
             (t (error "okänt tempus: ~s" tense)))))
    (unless (or (eq c :none) (member c *color*))
      (error "färgen ~s ligger utanför *color*" c))
    c))

;; När du talar om TID kvadreras triangeln: 3 linjer -> ruta med färg
(defmacro when-time (tense &body body)
  `(let ((*square* (choose-color ,tense)))
     ,@body))

;; Använda det:
(when-time :future
  (base57 43))   ; => (2 5) : 43 delat i 19-block ("43 square squares")
