> Draft

1. 80 chars limit
2. `let g:neomake_python_enabled_makers= ['python', 'pylama', 'flake8', 'pycodestyle', 'pydocstyle', 'pylint']`
3. Mostly [EAFP](https://stackoverflow.com/questions/11360858/what-is-the-eafp-principle-in-python)
4. Paranoid [duck typing](https://en.wikipedia.org/wiki/Duck_typing) (i.e. if
   you suspect this would be a pita to debug it's ok to sanity check)
5. Do not forget to `TODO`, `FIXME`, `NOTE` etc.
