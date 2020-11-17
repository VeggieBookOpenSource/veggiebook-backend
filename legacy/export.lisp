;;; -*- Mode:Lisp; Syntax:Common-lisp; Coding:utf-8; Package:QHMOBILE.EXPORT; Base:10 -*-

(in-package :cl-user)

#-SITEINIT.CL
(require :siteinit.cl "SYS:siteinit.cl")

(defmodule :qhmobile.export
  (:nicknames)
  (:use :common-lisp)
  (:requires :xmls
	     :edu.isi.isd.nlp.appl.xml.xmlsutil
	     :cl-ppcre
	     :edu.isi.isd.nlp.adt.list.histo
	     :edu.isi.isd.nlp.math.discrete.set
	     :edu.isi.isd.nlp.lang.control.caseutil)
  (:export)
  )

(in-package :qhmobile.export)

(defvar *master* (parse #P"/nfs/isd3/philpot/lisp/system/tailor/data/input/master/master-4.4.5.xml"))

(defun has-en-gate (node)
  (member '("Gate" "(AND (EQUIV $Lang :EN))")
	  (node-attrs node)
	  :test #'equal))

(defun ingredient-text (node)
  (flat-value node :delimiter #\space))

(defun step-text (node)
  (flat-value node :delimiter #\space))

(defun recipe-title (node &key (lang :en))
  (let ((title (find-node "Title" node)))
    (and title
	 (let* ((gate (format nil "(AND (EQUIV $Lang ~S))" lang))
		(text (find-node-attrmatch "Text" "Gate" gate title)))
	   (apply #'concatenate 'string
		  (node-children text))))))

(defun recipe-storyline (node &key (lang :en))
  (let ((storyline (find-node "Storyline" node)))
    (and storyline
	 (let* ((gate (format nil "(AND (EQUIV $Lang ~S))" lang))
		(text (find-node-attrmatch "Text" "Gate" gate storyline)))
	   (apply #'concatenate 'string
		  (node-children text))))))

(defun recipe-rid (node)
  (let ((rid (get-attribute node "Rid")))
    (unless rid
      (warn "Missing RID")) 
    rid))

(defun recipe-foodstuff (node)
  (let ((rid (recipe-rid node)))
    (and rid
	 (let ((abbrev (rid-to-abbrev rid)))
	   (abbrev-to-foodstuff abbrev)))))

(defun rid-to-abbrev (rid)
  (let ((abbrev (subseq rid 0 2)))
    abbrev))

(defun rid-to-ridx (rid)
  (let ((ridx (parse-integer rid :start 3 :junk-allowed t)))
    ridx))

(let ((assoc '(("BR" "BROCCOLI")
	       ("CB" "CABBAGE")
	       ("CA" "CARROT")
	       ("CL" "CAULIFLOWER")
	       ("GB" "GREENBEAN")
	       ("ON" "ONION")
	       ("PO" "POTATO")
	       ("RV" "ROOTVEGETABLE")
	       ("SW" "SWEETPOTATO")
	       ("ZU" "ZUCCHINI"))))
  (defun abbrev-to-foodstuff (rid)
    (second (assoc rid assoc :test #'equal))))

(let ((assoc '(("BR" 10)
	       ("CB" 11)
	       ("CA" 12)
	       ("CL" 13)
	       ("GB" 14)
	       ("ON" 15)
	       ("PO" 16)
	       ("RV" 17)
	       ("SW" 18)
	       ("ZU" 19))))
  (defun abbrev-to-kiid (abbrev)
    (second (assoc abbrev assoc :test #'equal))))

(defun harvest-characteristic (node ch &key (lang :en))
  (let ((gate (format nil "(AND (EQUIV $Lang ~S))" lang)))
    (dolist (c (find-nodes-attrmatch "Characteristic" "Gate" gate node))
      (let ((texts (node-children c)))
	(when (equal (first (node-children (first texts))) ch)
	  (return-from harvest-characteristic
	    (flat-value (second texts))))))))

(defun flat-value (node &key (delimiter #\space))
  (with-output-to-string (s)
    (let ((/needs/ nil))
      (declare (special /needs/))
      (flat-value-aux s node delimiter))))

(defun flat-value-aux (stream node delimiter)
  (declare (special /needs/))
  (cond ((nodep node)
	 (dolist (child (node-children node))
	   (flat-value-aux stream child delimiter)))
	(t
	 (when /needs/
	   (princ delimiter stream))
	 (write-string node stream)
	 (setq /needs/ t))))
	   

(defun en-to-boolean (en)
  (case-string-equal en
    ("yes" 1)
    ("no" 0)))

#+NOT
(defun recipe-good-for-leftovers (node)
  (let ((ch (harvest-characteristic node "Good for leftovers?"
				    :lang :en)))
    (en-to-boolean ch)))

(defun recipe-good-for-leftovers (node &key (lang :en))
  (let ((ch (harvest-characteristic 
	     node
	     (ecase lang
	       (:en "Good for leftovers?")
	       (:es (load-time-value 
		     (format nil "~ASe puede guardar lo que sobre?"
			     #\inverted_question_mark))))
	     :lang lang)))
    ch))

#+NOT
(defun recipe-can-be-made-ahead (node)
  (let ((ch (harvest-characteristic node "Can be made ahead?"
				    :lang :en)))
    (en-to-boolean ch)))

(defun recipe-can-be-made-ahead (node &key (lang :en))
  (let ((ch (harvest-characteristic 
	     node
	     (ecase lang
	       (:en "Can be made ahead?")
	       (:es (load-time-value 
		     (format nil "~ASe puede hacer de antemano?"
			     #\inverted_question_mark))))
	     :lang lang)))
    ch))

#+NOT
(defun recipe-can-be-frozen (node)
  (let ((ch (harvest-characteristic node "Can be frozen?"
				    :lang :en)))
    (en-to-boolean ch)))

(defun recipe-can-be-frozen (node &key (lang :en))
  (let ((ch (harvest-characteristic 
	     node
	     (ecase lang
	       (:en "Can be frozen?")
	       (:es (load-time-value 
		     (format nil "~ASe puede congelar?"
			     #\inverted_question_mark))))
	     :lang lang)))
    ch))

(defun recipe-servings (node &key (lang :en))
  (let ((ch (harvest-characteristic node (ecase lang
					   (:en "Servings:")
					   (:es "Porciones:"))
				    :lang lang)))
    ch))

#+NOT
(defun recipe-time-to-cook (node)
  (let ((ch (harvest-characteristic node "Cooking Time:"
				    :lang :en)))
    (parse-integer ch :junk-allowed t)))

(defun recipe-time-to-cook (node &key (lang :en))
  (let ((ch (harvest-characteristic node (ecase lang
					   (:en "Cooking Time:")
					   (:es "Tiempo para cocinar:"))
				    :lang lang)))
    ch))

#+NOT
(defun recipe-time-to-prepare (node)
  (let ((ch (harvest-characteristic node "Preparation Time:"
				    :lang :en)))
    (parse-integer ch :junk-allowed t)))

(defun recipe-time-to-prepare (node &key (lang :en))
  (let ((ch (harvest-characteristic 
	     node (ecase lang
		    (:en "Preparation Time:")
		    ;; (:es "Tiempo de preparación:")
		    (:es #.(format nil "Tiempo de preparaci~An:"
				   #\latin_small_letter_o_with_acute)))
	     :lang lang)))
    ch))

(defun export-recipe (node)
  (let* ((rid (recipe-rid node))
	 (abbrev (rid-to-abbrev rid))
	 (kiid (abbrev-to-kiid abbrev))
	 (ridx (rid-to-ridx rid))
	 (erid (+ (* kiid 1000) ridx)))
    ;; title
    (format t "~&t~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-title node :lang :en)
	    (recipe-title node :lang :es))
    (format t "~&t~D.save()" erid)
    ;; storyline
    (format t "~&l~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-storyline node :lang :en)
	    (recipe-storyline node :lang :es))
    (format t "~&l~D.save()" erid)
    ;; servings
    (format t "~&g~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-servings node :lang :en)
	    (recipe-servings node :lang :es))
    (format t "~&g~D.save()" erid)
    ;; ttc
    (format t "~&k~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-time-to-cook node :lang :en)
	    (recipe-time-to-cook node :lang :es))
    (format t "~&k~D.save()" erid)
    ;; ttp
    (format t "~&m~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-time-to-prepare node :lang :en)
	    (recipe-time-to-prepare node :lang :es))
    (format t "~&m~D.save()" erid)
    ;; cbma
    (format t "~&c~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-can-be-made-ahead node :lang :en)
	    (recipe-can-be-made-ahead node :lang :es))
    (format t "~&c~D.save()" erid)
    ;; cbf
    (format t "~&f~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-can-be-frozen node :lang :en)
	    (recipe-can-be-frozen node :lang :es))
    (format t "~&f~D.save()" erid)
    ;; gfl
    (format t "~&v~D = String(en='''~A''',es='''~A''')" 
	    erid
	    (recipe-good-for-leftovers node :lang :en)
	    (recipe-good-for-leftovers node :lang :es))
    (format t "~&v~D.save()" erid)
    ;; rid
    (format t "~%r~D = Recipe(rid=~D,title=t~D,storyLine=l~D,~
timeToPrepare=m~D,timeToCook=k~D,servings=g~D,canBeMadeAhead=c~D,~
canBeFrozen=f~D,goodForLeftovers=v~D,foodStuff=FoodStuff.objects.get(id='''~A'''))"

	    erid erid erid erid
	    erid erid erid 
	    erid
	    erid
	    erid
	    (recipe-foodstuff node))
    (format t "~&r~D.save()" erid)
    ;; ingredients
    (let ((ingredients (find-nodes "Ingredient" node)))
      (multiple-value-bind (ens ess) (partition-if #'has-en-gate ingredients)
	(if (and ens ess (= (length ens) (length ess)))
	    (loop for en in ens as es in ess as i from 1 by 1
		as iid = (+ i 100 (* erid 1000))
		do (format t "~&s~D = String(en='''~A''',es='''~A''')" 
			   iid
			   (ingredient-text en)
			   (ingredient-text es))
		do (format t "~&s~D.save()" iid)
		do (format t "~&i~D = RecipeIngredient(content=s~D,recipeId=r~D)"
			   iid iid erid)
		do (format t "~&i~D.save()" iid))
	  (warn "ingr problem ~D/~D with ~A" 
		(length ens) (length ess) rid))))
    (let ((steps (find-nodes "Step" node)))
      (multiple-value-bind (ens ess) (partition-if #'has-en-gate steps)
	(if (and ens ess (= (length ens) (length ess)))
	    (loop for en in ens as es in ess as i from 1 by 1
		as zid = (+ i 100 (* erid 1000))
		do (format t "~&s~D = String(en='''~A''',es='''~A''')" 
			   zid
			   (step-text en)
			   (step-text es))
		do (format t "~&s~D.save()" zid)
		do (format t "~&z~D = RecipeStep(content=s~D,recipeId=r~D)"
			   zid zid erid)
		do (format t "~&z~D.save()" zid))
	  (warn "step problem ~D/~D with ~A" 
		(length ens) (length ess) rid))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(cl:in-package :cl-user)

(defmodule :qhmobile.export
  (:nicknames)
  (:use :common-lisp)
  (:requires :xmls
	     :edu.isi.isd.nlp.appl.xml.xmlsutil
	     :cl-ppcre
	     :edu.isi.isd.nlp.adt.list.histo
	     :edu.isi.isd.nlp.math.discrete.set
	     :edu.isi.isd.nlp.lang.control.caseutil
	     :edu.isi.isd.nlp.adt.readtable.readtableutil
	     :edu.isi.isd.nlp.adt.hash-table
	     :edu.isi.isd.nlp.adt.list.flatten
	     :edu.isi.isd.nlp.adt.list.keep
	     :edu.isi.isd.nlp.adt.list.listutil
	     :edu.isi.isd.nlp.adt.file.csv.philpot)
  (:export)
  )

(cl:in-package :qhmobile.export)

(defun dollarp (symbol)
  (and (or (stringp symbol)
	   (symbolp symbol))
       (starts-with symbol "$")))

(defun indicatorp (symbol)
  (member symbol '(;; from RECIPE MAIN GATE
		   ;; ethnics
		   |$AgreeAsianCooking|
		   |$AgreeHispanicCooking|
		   |$AgreeSoulFoodCooking|
		   ;; ingreds
		   |$AgreeChicken| 
		   |$AgreeGarlic|
		   ;; food styles
		   |$AgreeSoup| 
		   ;; devices
		   |$HasConventionalOven| 
		   |$HasCrockPot|
		   |$HasJuicer| 
		   |$HasMicrowave|
		   |$HasSteamer|
		   |$HasToasterOven| 
		   ;; from ANNOTATIONS
		   |$AgreeKidFriendly|
		   ;; TIPS
		   |$AgreeDiabetes|
		   |$InterestedInPrepareSmallFamily|
		   |$InterestedInNutritionChild|
		   |$InterestedInSnacks|
		   |$InterestedInPrepareChild|
		   |$InterestedInNutritionAdultSenior|
		   |$InterestedInStorage|
		   |$InterestedInFreezing|
		   |$InterestedInNutritionGeneral|
		   |$InterestedInServing|
		   |$InterestedInSpoilage|
		   ;; IGNORE THESE
		   ;; |$Condition|
		   ;; |$Ingredient| 
		   ;; |$TotalTimeAllowed|
		   ;; |$Lang|
		   )))

(let ((indicators 
       (manifest-ht 'equal
	 ;; from RECIPE MAIN GATE
	 ;; ethnics
	 '|$AgreeAsianCooking| 1
	 '|$AgreeHispanicCooking| 2
	 '|$AgreeSoulFoodCooking| 3
	 ;; ingreds
	 '|$AgreeChicken| 11
	 '|$AgreeGarlic| 12
	 ;; food styles
	 '|$AgreeSoup| 21
	 ;; devices
	 '|$HasConventionalOven| 31
	 '|$HasCrockPot| 32
	 '|$HasJuicer| 33 
	 '|$HasMicrowave| 34
	 '|$HasSteamer| 35 
	 '|$HasToasterOven| 36 
	 ;; from ANNOTATIONS
	 '|$AgreeKidFriendly| 41
	 ;; TIPS
	 '|$AgreeDiabetes| 51
	 '|$InterestedInPrepareSmallFamily| 52
	 '|$InterestedInNutritionChild| 53
	 '|$InterestedInSnacks| 54
	 '|$InterestedInPrepareChild| 55
	 '|$InterestedInNutritionAdultSenior| 56
	 '|$InterestedInStorage| 57 
	 '|$InterestedInFreezing| 58
	 '|$InterestedInNutritionGeneral| 59
	 '|$InterestedInServing| 60 
	 '|$InterestedInSpoilage| 61
	 ;; IGNORE THESE
	 ;; |$Condition|
	 ;; |$Ingredient| 
	 ;; |$TotalTimeAllowed|
	 ;; |$Lang|
	 )))
  (defun indicators () indicators)
  (defun indicatorp (x) (not (null (gethash x indicators))))
  (defun indicator-idx (x) (and (indicatorp x)
				(values (gethash x indicators))))
  (defun indicator-lessp (x y)
    (< (indicator-idx x) (indicator-idx y)))
  )

(defun get-gate-expression (r)
  (and r
       (let ((a (get-attribute r "Gate")))
	 (and a
	      (with-case-preserving-readtable ()
		(canon-list (read-from-string a)))))))

(defun recipe-rid (r)
  (or (get-attribute r "Rid")
      (error "No RID for recipe ~S" r)))

(defun recipe-id (r)
  (or (get-attribute r "Id")
      (error "No ID for recipe ~S" r)))

(defstruct gatesyms
  rid
  id
  main
  annot
  all)

(defun get-all-gates ()
  (let ((ht (make-hash-table :test #'equal)))
    (dolist (r (find-nodes "Recipe" *master*))
      (let* ((rid (recipe-rid r))
	     (id (recipe-id r))
	     (gs (make-gatesyms :rid rid :id id)))
	(setf (gethash rid ht) gs)
	;; first get known ingredient/device/ethnics
	(setf (gatesyms-main gs)
	  (remove-duplicates
	   (keep-if #'dollarp
		    (flatten
		     (get-gate-expression r)))))
	;; second get kid friendly from annotations' gates
	(dolist (a (find-nodes "Annotation" r))
	  (setf (gatesyms-annot gs)
	    (nunion (gatesyms-annot gs)
		    (remove-duplicates
		     (keep-if #'dollarp
			      (flatten
			       (get-gate-expression a)))))))
	;; third get all 	
	(let ((s (list)))
	  (do-all-descendants (n r)
	    (when (nodep n)
	      (setq s (nunion s (get-gate-expression n)))))
	  (setf (gatesyms-all gs) 
	    (remove-duplicates
	     (keep-if #'dollarp
		      (flatten s)))))))
    ht))

(defun check (a b)
  (warn "~A ~A" a b))

;;; Array dimensions A[recipes, indicators]

(defun gates-to-excel (gates &key (file "/tmp/excel.csv"))
  (let ((columns (list)))
    (maphash #'(lambda (i v)
		 (push (list i v nil) columns))
	     (indicators))
    (setq columns (sort columns #'< :key #'second))
    (loop for column in columns
	as m from 2 by 1
	do (setf (third column) m))
    (setf columns (list* (list 'rid -1 0)
			 (list 'id -1 1)
			 columns))
    (let ((m (make-array (list (1+ (hash-table-count gates))
			       (length columns))
			 :initial-element 0)))
      (loop for (name nil j) in columns
	  do (setf (aref m 0 j) (symbol-name name)))
      (flet ((check (indic pair)
	       (let ((i (third (assoc indic columns)))
		     (key (car pair))
		     (k (cdr pair)))
		 #+ignore
		 (warn "~A ~A ~A ~A"
		       indic i
		       key k)
		 (setf (aref m k i) 1)))) 
	(let ((keys (ht-keys gates)))
	  (setq keys (sort keys #'string<))
	  (loop for key in keys
	      as k from 1 by 1
	      as gs = (gethash key gates)
	      do (setf (aref m k 0) (gatesyms-rid gs)
		       (aref m k 1) (gatesyms-id gs))
	      do (dolist (i (gatesyms-main gs))
		   (when (indicatorp i)
		     (check i (cons key k))))
	      do (dolist (i (gatesyms-annot gs))
		   (when (indicatorp i)
		     (check i (cons key k))))
	      do (dolist (i (gatesyms-all gs))
		   (when (indicatorp i)
		     (check i (cons key k)))))))
      (values (array-to-csv m file)
	      m))))
