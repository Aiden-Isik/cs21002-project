#!/usr/bin/env guile
!#
;;; Environment variables to be passed to the shell.
;;; This is a hack to get around the fact that (system*) does not
;;; seem to inherit certain environment variables, so guix shell's
;;; --inherit does not pass them through properly, and the simulator
;;; fails to start.
(define env-vars
  (string-append
   "DISPLAY=" (getenv "DISPLAY") " "
   "XDG_RUNTIME_DIR=" (getenv "XDG_RUNTIME_DIR") " "
   "XAUTHORITY=" (getenv "XAUTHORITY") " "))

;;; Execute the following command to start the simulator
(system*
 "guix" "shell" "--container"
 ;; Pass through the Direct Rendering Infrastructure device to the shell
 "--expose=/dev/dri"
 ;; Pass through rendering-related directories to the shell
 "--share=/tmp/.X11-unix/"
 (string-append "--expose=/run/user/" (number->string (getuid)))
 ;; Install python, pyglet, gymnasium, numpy, and bash to the shell
 "python" "python-pyglet" "python-gymnasium" "python-numpy" "bash-minimal"
 ;; Run the python interpreter after passing environment variables
 "--" "sh" "-c" (string-append env-vars "python3 \"" (dirname (current-filename)) "/src/main.py\""))
