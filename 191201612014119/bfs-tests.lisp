;; BFS Tests

(let ((bad-node nil))

  (defun test-path (path node end net)
    (setq bad-node end)
    (assert-equal path
                  (shortest-path node end net)))
  
  (defun empty-queue-p (queue)
    (when (some (lambda (path) (member bad-node path)) queue)
      (fail "Path with ~S put in queue" bad-node))
    (null queue))
  )

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
  (test-path '() 'a 'f '((a b c) (b c) (c b) (e f)))
  (test-path '(a b c e f) 'a 'f '((a b) (b c d) (c e) (d a) (e f)))

  )
