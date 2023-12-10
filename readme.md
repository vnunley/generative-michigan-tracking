# Michigan Tracking Exercise

This Python project generates a PDF for the Michigan Tracking Exercise, a physical therapy exercise often used in the treatment of concussions. The program can generate exercises in both English and Hebrew.

### Disclaimer
Please note that this exercise is not evaluated by a doctor and is not intended to diagnose, treat, cure, or prevent any disease or health condition. Always consult with a healthcare provider for medical advice.

### Importing and Using in Other Projects
To use this project in another Python application, you can import the `generate_exercises` function from the `main.py` file. This function generates a number of exercises, each containing a set of gibberish words. The number of exercises and the number of words in each exercise are specified by the parameters. The language parameter determines the language of the words, and the filename parameter specifies the name of the output file. If the caps parameter is set to True, the words will be in uppercase.

Here is an example of how to use it:

```python
from generative-michigan-tracking import generate_exercises

generate_exercises(60, 10, 'en', True, 'output.pdf')
```

### Running the Project Locally
To run this project locally, you will need to have Python installed on your machine.

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following commands:

```
make install
make run
```

The `make install` command sets up a virtual environment and installs the necessary Python packages as specified in the `requirements.txt` file. The make run command activates the virtual environment and runs the `main.py` script to generate the PDF.

After running these commands, you should see a file named `output.pdf` in your project directory. This file contains the Michigan Tracking Exercise.

### License

This project is licensed under the GNU General Public License v3.0. For more details, please see the LICENSE file.