;-----------------------------Requirement-----------------
;State space search formalizes solving many problems as starting with some initial state S, and trying different actions that lead to new states, until you find a state that satisfies some goal predicate P. The solution is a list of states, called a path, showing the states from the final goal backward to the initial state.
;Generalize the BFS function to do simple breadth-first state space search. Define (bfs paths pred gen) to take three arguments:
;paths - A list of paths, where each path is a list of states, from newest to oldest
;pred - A predicate that takes a state and returns true if the state is a goal state
;gen - A predicate that takes a path and returns the list of states that can be reached legally from the first state in the path, given the other states in the path.

;bfs should avoid cycles, i.e., it should not add a state to any path twice. The gen function does not need to handle that case.


;------------------------------Code and Comments------------

(defun get-reachable-paths (path gen)
  (do ((neighbors (funcall gen path) (cdr neighbors))
       (new-paths nil (if (member (car neighbors) path)
                          new-paths
                        (acons (car neighbors) path new-paths))))
      ((null neighbors) new-paths)))
;;Use (mapcan #'(lambda (x) (if ... (list ...) nil)) lst)
;;when you want a list of just some calculated values. But in this case, you don't want this helper
;;Don't use a loop to generate a list for another loop. Make the main loop below use a conditional to skip cycles without consing a list of legal nodes

(defun bfs (paths pred gen)
  (if (null paths)
;;empty-queue-p doesn't work for generalized BFS. It doesn't have access to pred to test for the goal state.
      nil
    (do 
        ((reachable-paths (get-reachable-paths (car paths) gen) (cdr reachable-paths))
         (next-paths (reverse (cdr paths))  (cons (car reachable-paths) next-paths)))
        ((or (null reachable-paths)
             (funcall pred (caar reachable-paths)))
         (write reachable-paths) (terpri)
         (write next-paths) (terpri)
         (if (null reachable-paths)
             (bfs (reverse next-paths) pred gen)
           (car reachable-paths))))))
;;It's shorter and faster to use the C...R shortcut functions than explicit chains of CAR's and CDR's. See page 40 of Graham.
;;Don't create paths until you know you need them. If you see the goal. only one path is needed. If not, then you need them

(defun shortest-path (start end net)
  (write (list (list start))) (terpri)
  (reverse (bfs
            (list (list start))
            (lambda (state) (eql state end))
            (lambda (path) (cdr (assoc (car path) net))))))