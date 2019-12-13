;-----------------------Requirements---------------------
;;Define show-list to act like Lisp's PRINT, except that it should print square brackets instead of parentheses. (Printing to a string and replacing parentheses doesn't count.)

;;Define show-dots that takes a list and prints it in dot notation:

;------------------------Code and Comments--------------------
(defun show-dots (lst)
  (format t "~A" (showdots-rules lst)))

(defun showdots-rules (lst)
  (if (atom lst)
      lst
    (format nil "(~A . ~A)" (showdots-rules (car lst)) (showdots-rules (cdr lst)))))
;;This builds strings in order to print. It's just as simple, and much more efficient, to print as you go. No helper needed.

(defun show-list (lst)
  (show-list-rules lst t))

(defun show-list-rules (lst is-head)
;;Flag variables in loops (iterative or recursive) are tricky to maintain. There's almost always a more direct solution. http://martinfowler.com/bliki/FlagArgument.html http://www.informit.com/articles/article.aspx?p=1392524
  (cond ((null lst) (format t (if is-head "NIL" "")))
        ((and (atom lst) is-head) (format t "~a" lst))
        ((atom lst) (format t " . ~a" lst))
        (is-head
         (format t "[")
         (show-list-rules (car lst) t)
         (show-list-rules (cdr lst) nil)
         (format t "]"))
        (t
         (format t " ")
         (show-list-rules (car lst) t)
         (show-list-rules (cdr lst) nil))))
;;;The logic for list notation is only slightly more complex than dot notation: If atom, print it else print [ then the car then loop printing space + element until atom, then print . atom if not nil, then ]. That can be done with a top-level function tht handles the basic atom vs list, and a helper for the loop inside a list