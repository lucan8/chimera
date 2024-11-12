# Chimera

This project aims to determine the programming language used in a given input file
without relying on the file extension.

Supported languages:
- C++
- Java
- Rust

# Samples

This project includes scripts for data collection and the results obtained,
but not the projects themselves.
The projects used are listed in the References section.

The results of the data parsing are located at "chimera/data-parser/{language}_tokens.txt".
You can modify what tokens should be considered by modifying the file "chimera/data_parser/{language}_keywords.txt".

# Project structure

To use your sample data create a `cpp`, `rs` and `java` drectory inside "chimera/data-parser/samples",
your tree should look something like this:
```bash
.
├── cpp_results.txt
├── java_results.txt
├── keywords.txt
├── main.py
├── parser.py
├── README.md
├── requirements.txt
├── rs_results.txt
├── samples
│   ├── cpp-repo
│   ├── java-repo
│   └── rust-repo
└── tests.txt
```

# Run locally
```bash
git clone git@github.com:lucan8/chimera.git
cd chimera
pip install -r requirements.txt

// To run with your own training date make sure to follow the the
// information presented in "Project structure".

python3 main.py
```

To add your own samples do the following:
```bash
cd chimera
mkdir samples
cd samples

git clone <ssh_for_project1> --depth=1
git clone <ssh_for_project2> --depth=1

// Analyze the new projects
python3 parser.py

python3 main.py
...
```

# References
- For C++: https://github.com/opencv/opencv
- For Java: https://github.com/plantuml/plantuml
- For Rust: https://github.com/zed-industries/zed
