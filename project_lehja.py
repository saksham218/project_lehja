import json
import os
import shutil
import requests
import subprocess
        

class DataLoader:
    def __init__(self):
        pass
    
    def get_metadata(self,directory):
        print("Getting Metadata")
        response = requests.get("https://data-collection-backend.onrender.com/metadata/getAllMetadata")

        if response.status_code != 200:
            raise Exception(f"Failed to get metadata: {response.status_code} - {response.text}")
        metadata = response.json()

        # write
        with open(f"{directory}/metadata.json", "w") as file:
            json.dump(metadata, file, indent=4,default=str)
            # print(f"metadata downloaded successfully to {directory} folder")
        
        return metadata
    
    def get_blob(self,blob_name,directory):
        response = requests.get(f"https://sakshamdatacollection.blob.core.windows.net/datacollection/{blob_name}")
        
        if response.status_code == 200:
            with open("temp_audio.wav", "wb") as file:
                file.write(response.content)
                # print(f"{blob_name} downloaded successfully to {directory} folder")

            subprocess.run(['ffmpeg', '-i', "temp_audio.wav", '-acodec', 'pcm_s16le', f"{directory}/{blob_name}.wav"])
            os.remove("temp_audio.wav")

            # with wave.open(f"{directory}/{blob_name}.wav", "wb") as wav_file:
            #     # Set the WAV file parameters
            #     # Number of audio channels (1 for mono, 2 for stereo)
            #     n_channels = 2
            #     # Sample width in bytes (1 for 8-bit audio, 2 for 16-bit audio, etc.)
            #     sample_width = 2
            #     # Sampling frequency
            #     frame_rate = 22050
            #     # Number of frames
            #     n_frames = len(response.content) // sample_width

            #     # Set the WAV file parameters
            #     wav_file.setparams((n_channels, sample_width, frame_rate, n_frames, "NONE", "not compressed"))

            #     # Write audio data to the WAV file
            #     wav_file.writeframes(response.content)
        else:
            print(f"Failed to download blob: {response.status_code} - {response.text}")

    def get_data(self):
        print("Getting Data")
        directory = "data"
        # create directory if not present and delete the directory if already present
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{directory} directory created")
        else:
            shutil.rmtree(directory)
            print(f"{directory} directory deleted")
            os.makedirs(directory)
            print(f"{directory} directory created")

        metadata = self.get_metadata(directory)
        number_of_documents = len(metadata)
        print("Number of documents:",number_of_documents)

        for index,doc in enumerate(metadata):
            print("index: ",index+1,"/",number_of_documents)
            # print(doc)
            for language in doc['languages']:
                # print(language['controlledLanguageBlobName'])
                # print(language['ownLanguageBlobName'])
                if language['controlledLanguageBlobName'] != None:
                    self.get_blob(language['controlledLanguageBlobName'],directory)
                if language['ownLanguageBlobName'] != None:
                    self.get_blob(language['ownLanguageBlobName'],directory)
        
        
    def verify_data(self):
        print("Verifying Data")
        directory = "data"
        metadata = json.load(open(f"{directory}/metadata.json"))
        number_of_documents = len(metadata)

        print("Number of documents: ",number_of_documents)

        for index,doc in enumerate(metadata):
            print("index: ",index+1,"/",number_of_documents)
            for language in doc['languages']:
                if language['controlledLanguageBlobName'] != None:
                    with open(f"{directory}/{language['controlledLanguageBlobName']}.wav", "rb") as file:
                        # print(f"{language['controlledLanguageBlobName']} found")
                        pass
                if language['ownLanguageBlobName'] != None:
                    with open(f"{directory}/{language['ownLanguageBlobName']}.wav", "rb") as file:
                        # print(f"{language['ownLanguageBlobName']} found")
                        pass
        print("Data Verified Successfully")

    def get_number_of_submissions(self):
        response = requests.get("https://data-collection-backend.onrender.com/metadata/getNumberOfSubmissions")
        if response.status_code != 200:
            raise Exception(f"Failed to get number of submissions: {response.status_code} - {response.text}")
        number_of_submissions = response.json()
        print(number_of_submissions)

        return number_of_submissions




        

    

    
    
    
   