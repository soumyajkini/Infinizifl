;;----------------------------------------Code and Comments----------------------------------------

(defun get-reachable-paths (path gen)
  (do ((neighbors (funcall gen path) (cdr neighbors))
       (new-paths nil (if (member (car neighbors) path)
                          new-paths
                        (acons (car neighbors) path new-paths))))
      ((null neighbors) new-paths)))
;;Don't use a loop to generate a list for another loop. Make the main loop use the same logic to get the values needed without consing a list.

(defun has-solution-p (result)
  (cond ((null result) nil)
        ((eql 'dl result) nil)
        (t t)))

(defun dls (path pred gen n)
  (cond ((funcall pred (car path)) path)
;;Because of how iterative deepening works, you only need to call the goal predicate when you hit the new depth. All previous layers have been checked.
        ((< n (length path)) 'dl)
        (t (do* ((result
                  nil
                  (dls (car reachable-paths) pred gen n))
                 (was-dl
                  nil
                  (or was-dl (eql 'dl result)))
                 (reachable-paths
                  (get-reachable-paths path gen)
                  (cdr reachable-paths)))
                ((or (null reachable-paths) (has-solution-p result))
                 (cond ((has-solution-p result) result)
                       (was-dl 'dl)
                       (t nil)))))))
;;Hint: both NIL and a path are lists, so use that to signal "an answer has been found" and use some non-nil atom to signal "answer unknown". This simplifies the testing in the loops. No need for a helper like has-solution-p
;;Call pred on each node BEFORE consing onto the list of states.

(defun ids (paths pred gen)
  (do ((limit 1 (1+ limit)) 
       (result 'dl (dls (car paths) pred gen limit)))
      ((not (eql 'dl result)) result)))

(defun shortest-path (start end net)
  (reverse (ids
            (list (list start))
            (lambda (state) (eql state end))
            (lambda (path) (cdr (assoc (car path) net))))))


;; ---------------------------------------Tests ----------------------------------------------
(define-test shortest-path
  ;; Without cycles
    
  (test-path '(a c d) 'a 'd '((a b c) (b c) (c d)))
  (test-path '(a c) 'a 'c '((a b c) (b c) (c d)))
  (test-path '(a c d) 'a 'd '((a b c) (b e) (e c) (c d)))
  (test-path '(a c e f) 'a 'f '((a b c) (b c) (c e) (e f)))
  (test-path '(a b f) 'a 'f '((a b c) (b c f) (c e) (e f)))
  (test-path '()  'a 'f '((a b c) (b c) (c d) (e f)))
  (test-path '(a b f) 'a 'f '((a b c d) (b e f)))
  
  ;; With cycles
  (test-path '(a c d) 'a 'd '((a b c) (b a c) (c d)))
  (test-path '(a c) 'a 'c '((a b c) (b c) (c a d)))
  (test-path '() 'a 'c '((a b) (b a) (c)))
  (test-path '() 'a 'f '((a b c) (b a c) (c d) (e f)))
  (test-path '() 'a 'f '((a b c) (b c) (c b) (e f))))
