import subprocess
import os
import shutil

def rasa_init():
    try:
        # Specify the desired project directory name
        project_name = "rasa"
        rasa_directory = os.path.join(os.getcwd(), project_name)
        # Check if the folder exists
        if os.path.exists(rasa_directory) and os.path.isdir(rasa_directory):
            try:
                # Use shutil.rmtree to remove the entire directory
                shutil.rmtree(rasa_directory)
            except Exception as e:
                print(f"Error deleting the 'rasa' folder - {e}")
        else:
            print(f"The 'rasa' folder does not exist or is not a directory.")
        # Create the project directory if it doesn't exist
        if not os.path.exists(rasa_directory):
            os.mkdir(rasa_directory)
        else:
            print(f"Project directory already exists: {rasa_directory}")
        try:
            # Change the working directory to the "rasa" subfolder
            os.chdir(rasa_directory)
            # Run the Rasa init command
            subprocess.run(["rasa", "init", "--no-prompt"], check=True)
            print("Rasa project initialized successfully in", rasa_directory)
        except subprocess.CalledProcessError:
            print("Error occurred while initializing the Rasa project.")

        finally:
            # Return to the main directory
            os.chdir(os.path.dirname(rasa_directory))
        return True 
    except Exception as e:
        return False