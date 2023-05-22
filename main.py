import tkinter as tk
from PIL import Image, ImageTk
import csv
from azure.storage.blob import BlobServiceClient
import os
import os
import requests
from azure.storage.blob import BlobServiceClient


# Your Azure storage information
storage_account_name = "saanchorwatch"
storage_account_key = "9k+TdznJXqnKsbO+gY9vGWaXM9cFPQMeWjExktohgiwVQYOAsHaVICmdtNBBelIkLy2VChcDHvgl+AStd18b+Q=="
container_name = "pictures"

# Create a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

# Azure container URL
container_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}"



def get_images_url():
    account_name = 'saanchorwatch'
    account_key = '9k+TdznJXqnKsbO+gY9vGWaXM9cFPQMeWjExktohgiwVQYOAsHaVICmdtNBBelIkLy2VChcDHvgl+AStd18b+Q=='
    container_name = 'pictures'

    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()

    photo_urls = []

    for blob in blobs:
        photo_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}"
        photo_urls.append(photo_url)

    photo_urls = photo_urls[::-1]
    print(photo_urls)
    print(len(photo_urls))
    return photo_urls

# Function to download and save images from Azure container
def download_images_from_azure(num_images):
    # Create a directory to save the images
    os.makedirs("downloaded_images", exist_ok=True)

    image_urls = get_images_url()
    # Download and save the images
    for i in range(min(num_images, len(image_urls))):
        image_url = image_urls[i]
        image_name = f"image{i+1}.jpg"
        image_name = image_url[53:]

        print(image_name)
        image_path = os.path.join("downloaded_images", image_name)

        response = requests.get(image_url)
        with open(image_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded image: {image_path}")


# Call the function to download and save images
num_images_to_download = 100
download_images_from_azure(num_images_to_download)

# List of image file names
images = [
    "Grindebacken-2023-05-1520_09_23.jpg",
    "Grindebacken-2023-05-1520_00_52.jpg",
    "Grindebacken-2023-05-1520_11_30.jpg",
    "ndjsnefn.jpg"
]
images = os.listdir("downloaded_images")
images.append("null.jpg")

images_done = []

# CSV file name to save the information
csv_file = "boat_counts.csv"

# Create the Tkinter window
window = tk.Tk()

# Create a Tkinter label to display the image
image_label = tk.Label(window)
image_label.pack()

# Create a Tkinter entry to input the boat count
count_entry = tk.Entry(window)
count_entry.pack()
# Create a list to store the boat counts
boat_counts = []




# Function to save the information to the CSV file and terminate the program
def save_information():
    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the boat counts to the CSV file
        writer.writerows(boat_counts)

    # Close the Tkinter window
    window.destroy()

# Function to display the next image
def display_image():
    print(images)
    print(images_done)

    # Get the next image from the list
    image_name = images.pop(0)
    images_done.append(image_name)

    # Display the image in the Tkinter window
    image = Image.open("downloaded_images/" + image_name)
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo

    # Enable the entry and submit button
    count_entry.configure(state='normal')
    submit_button.configure(state='normal')

# Function to handle the submit button click
def submit_count():
    if len(images) > 1:
        # Get the boat count entered by the user
        count = count_entry.get()

        # Add the image name and boat count to the list
        boat_counts.append([images_done[-1], count])

        # Clear the entry
        count_entry.delete(0, 'end')

        # Disable the entry and submit button
        count_entry.configure(state='disabled')
        submit_button.configure(state='disabled')

        # Display the next image
        display_image()
    else:
        # Get the boat count entered by the user
        count = count_entry.get()

        # Add the image name and boat count to the list
        boat_counts.append([images_done[-1], count])

        # Clear the entry
        count_entry.delete(0, 'end')

        # Disable the entry and submit button
        count_entry.configure(state='disabled')
        submit_button.configure(state='disabled')
        save_information()

# Configure the submit button click event


# Create a Tkinter button to finish the program
# Create a Tkinter button to finish the program
finish_button = tk.Button(window, text="Finish", command=save_information)
finish_button.place(x=450, y=480)

# Create a Tkinter button to submit the boat count
submit_button = tk.Button(window, text="Submit", command=submit_count)
submit_button.place(x=400, y=480)

submit_button.configure(command=submit_count)

# Disable the entry and submit button initially
count_entry.configure(state='disabled')
submit_button.configure(state='disabled')

# Start the program by displaying the first image
display_image()

#

# Run the Tkinter event loop
window.mainloop()

# Get the boat count entered by the user