# Fourier Transformer

Create a path and draw it using awesome Fourier series.

## Getting Started
1. Python3 is needed.
2. If pygame is not installed, run `pip install pygame`
3. Get into the project directory.
4. Run `python main.py` to start the demo: a square.

## Create your own path
1. Get into the project directory.
2. Run `python create_path.py`. This will start a gui, and you can draw your path there.
   After that, click the save button to save it into `path/to/your/file`.
3. Run `python main.py --path-file "path/to/your/file"`.

## Generate path from svg file
1. Get into the project directory.
2. Run `python svg_to_path.py --file-name "path/to/your/file"`, then the path file has the same name as the svg file will be placed beside the svg file. if there're multiple paths in the svg file, they will be put in a directory.
3. if you only want to generate one path, you can use `python svg_to_path.py --file-name "path/to/your/file" --path-index <the number>`

Just enjoy !