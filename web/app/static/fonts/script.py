import os
files = os.listdir('.')
css = "@font-face {{ font-family: {0} ;  src: url({1}); }}\n"

with open ('../css/style.css', 'a') as f:
    for file in files: 
        f.write(css.format(file.rsplit( ".", 1 )[ 0 ], '../fonts/' + file))
       