import React, { useState } from 'react';

// Define the type for the component's props
interface FileUploadProps {
  uploadUrl: string; // The backend endpoint URL
  label: string;      // A label for this specific uploader (e.g., "Player Data")
}

function FileUpload({ uploadUrl, label }: FileUploadProps): JSX.Element {
  // State hooks with explicit types
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Handles file selection - type the event
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // event.target.files can be null
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    } else {
      setSelectedFile(null);
    }
    setStatusMessage(''); // Clear previous messages
  };

  // Handles the file upload submission - type the event
  const handleUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent default form submission

    if (!selectedFile) {
      setStatusMessage('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setStatusMessage('Uploading...');

    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('file', selectedFile); // 'file' matches the key Flask expects

    try {
      // Send the POST request to the backend
      const response = await fetch(uploadUrl, { // Use the prop for the URL
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json', // We expect JSON response (especially for errors)
        },
      });

      // Check if the request was successful
      if (!response.ok) {
        // Try to parse error message from backend if available
        let errorMessage = `Upload failed with status: ${response.status}`;
        try {
          const errorData: { error?: string } = await response.json(); // Type the expected error structure
          errorMessage = errorData.error || errorMessage;
        } catch (parseError) {
          // Ignore if response is not JSON or doesn't match structure
          console.debug("Could not parse error response as JSON", parseError);
        }
        throw new Error(errorMessage);
      }

      // Handle successful upload (optional: process response if backend sends data)
      // const result = await response.json();
      setStatusMessage(`File "${selectedFile.name}" uploaded successfully!`);
      setSelectedFile(null); // Clear the file state
      
      // Reset file input visually by resetting the form
      if (event.currentTarget) {
          event.currentTarget.reset();
      }


    } catch (error: unknown) { // Catch unknown type for better error handling
      console.error('Upload error:', error);
      if (error instanceof Error) {
        setStatusMessage(`Upload failed: ${error.message}`);
      } else {
        setStatusMessage('An unknown upload error occurred.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <h3>Upload {label}</h3>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".csv,.xlsx,.html" // Specify acceptable file types
          onChange={handleFileChange}
          disabled={isLoading}
          aria-label={`Select file for ${label}`} // Accessibility
        />
        <button type="submit" disabled={isLoading || !selectedFile}>
          {isLoading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {statusMessage && <p className="status-message">{statusMessage}</p>}
    </div>
  );
}

export default FileUpload;
