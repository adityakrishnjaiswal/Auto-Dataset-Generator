import React, { useState } from 'react';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import logo from './logo.jpeg'; // Import your logo image

function FileUploadForm() {
    const [videoFile, setVideoFile] = useState(null);
    const [referenceFiles, setReferenceFiles] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [downloading, setDownloading] = useState(false); // New state for download

    const handleVideoChange = (e) => {
        setVideoFile(e.target.files[0]);
    };

    const handleReferenceChange = (e) => {
        setReferenceFiles([...e.target.files]);
    };

    const uploadFiles = async () => {
        if (!videoFile || referenceFiles.length === 0) {
            alert('Please upload both video and reference images.');
            return;
        }

        const formData = new FormData();
        formData.append('video', videoFile);
        referenceFiles.forEach((file) => {
            formData.append('references', file);
        });

        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                setMessage(result.message || 'Upload successful');
            } else {
                const errorDetails = await response.json();
                setMessage(errorDetails.error || 'Failed to upload files.');
            }
        } catch (error) {
            console.error('Error:', error);
            setMessage('Upload failed due to an error.');
        } finally {
            setLoading(false);
        }
    };

    const generateDataset = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/process', {
                method: 'POST',
            });

            if (response.ok) {
                setMessage("Generating Dataset. It'll take some time....");
            } else {
                const errorData = await response.json();
                setMessage(errorData.error || 'Processing failed!');
            }
        } catch (error) {
            console.error('Error during dataset generation:', error);
            setMessage('An error occurred during processing.');
        } finally {
            setLoading(false);
        }
    };

    const downloadDataset = async () => {
        setDownloading(true); // Start loading indicator
        try {
            const response = await fetch('http://127.0.0.1:5000/download', {
                method: 'GET',
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'datasets.zip';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else {
                const errorDetails = await response.json();
                setMessage(errorDetails.error || 'Failed to download dataset.');
            }
        } catch (error) {
            console.error('Error:', error);
            setMessage('Download failed due to an error.');
        } finally {
            setDownloading(false); // Stop loading indicator
        }
    };

    return (
        <div className="container">
            {/* Header with logo */}
            <header className="header">
                <img src={logo} alt="Logo" className="logo" />
                <h1 className="header-title">YOLO Dataset Generator</h1>
            </header>
    
            {/* Main form section */}
            <div className="form-container">
                <h2>Upload Video and Reference Images</h2>
                <form>
                    <div className="form-group">
                        <label className="label">Video File:</label>
                        <input type="file" onChange={handleVideoChange} required className="input" /><br /><br />
    
                        <label className="label">Reference Images:</label>
                        <input type="file" multiple onChange={handleReferenceChange} required className="input" /><br /><br />
    
                        <button type="button" onClick={uploadFiles} disabled={loading} className="button">
                            {loading ? 'Uploading...' : 'Upload'}
                        </button>
                    </div>
                </form>
    
                <h2>Generate Dataset</h2>
                <button type="button" onClick={generateDataset} disabled={loading} className="button">
                    {loading ? 'Generating...' : 'Generate'}
                </button>

                {/* Linear progress indicator */}
                {loading && (
                    <Box sx={{ width: '100%', marginTop: 2 }}>
                        <LinearProgress />
                    </Box>
                )}
    
                <h2>Download Dataset</h2>
                <div className="download-container">
                    <button type="button" onClick={downloadDataset} disabled={loading} className="button">
                        {loading ? 'Downloading...' : 'Download'}
                    </button>
                    {downloading && <div className="loading-icon"></div>} {/* Loading icon */}
                </div>
    
                <div className="message">{message}</div>
            </div>
        </div>
    );
}

export default FileUploadForm;
