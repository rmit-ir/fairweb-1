# fairweb-1
CIDDA RMIT IR participation at the NTCIR FairWeb-1 task

## To clone the private repository via terminal, you can follow these steps:

1. Open the terminal on your Linux machine.
   
   ```
   cd ~
   ```
2. Generate an SSH key (if you haven't already) by using the command:

   ```
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
   Follow the prompts to generate the key pair. 
   Note: Instead of overwriting the existing rsa file, it is recommended to create a new one.
4. Add your SSH key to your GitHub account by copying the contents of the public key to your clipboard (i.e., from the newly created pub.key). 
   You can use the command:
   
   ```
   cat ~/.ssh/id_rsa.pub
   ```
   
   This command will output the contents of your public key to the terminal. Copy the entire output to your clipboard.<br>
   Then, go to your GitHub account settings, click on "SSH and GPG keys", and click on "New SSH key". <br>
   Give the key a descriptive title and paste the contents of your public key into the "Key" field. Click "Add SSH key" to save it.
5. Then in the terminal, go to the directory where you want the repository cloned and enter the following command to clone:
   
   ```
   git clone git@github.com:rmit-ir/fairweb-1.git
   ```
   
   Enter your passphrase if/when prompted.

**Note:** Make sure you have appropriate access permissions and authentication credentials (such as an SSH key) before attempting to clone a private repository.

## Steps to test run the evaluation

1. Go the NTCIREVAL folder and enter the following command:
   ```
   make
   ```
   You should see `gcc -o ntcir_eval ntcir_eval.o -lm` on your terminal as a result.
   Now, to test that the evaluation scripts are working, lets go to the folder named `toy`
2. Run the following command:
   ```
   ./run_eval_script.sh
   ```
   This should generate files with the following suffix, `.tid`, `GFRnev`, and folders `P001`, `P002`, `P003`, `P004` i.e., based on the number of topics and the `results` folder which will contain all the `.tsm` files which contain the scores. More details about the scores will be explained in a later section. Please open one of the `.tsm` file in the results folder and ensure the values are not 0 or the file is not empty.
   Also, If you want to clear all the generated files, you may also use the following command:
   ```
   ./clear_generations.sh
   ```
   **Note:** Please do make sure the above mentioned shell scripts have `execute` permissions. For example, this can be done by the following command:
   ```
   chmod +x run_eval_script.sh
   ```
   
   ```
   chmod +x clear_generations.sh
   ```
   You have succesfully run the evaluation on the `toy` dataset.
   
## Training Data and Baseline runs

1. Go to the folder `FW1pilotpack`
2. The organizers have provided the following baseline run files which are available in this folder.
   ```
   run.qld-depThre6
   run.qljm-depThre6
   run.bm25-depThre6
   ```
3. The evaluation script runs on all the runs named in the file `runlist`.
4. Run the following command to evaluate all the runs named in the file `runlist`
   ```
   ./run_eval_script.sh
   ```
5. If all the files are generated successfully for existing runs, you may add your own runs to this folder for evaluation.
6. Add the run name to the the `runlist` file.
   
