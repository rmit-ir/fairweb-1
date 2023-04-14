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
