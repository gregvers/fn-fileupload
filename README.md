# fn-fileupload
function that provides a web page to upload a file to a bucket using a pre-authenticated request

A static HTML page (not included) displays a form requesting for the presenter name and session ID.
Once submitted, a POST calls for the fn-fileupload function that return another HTML page to select the file to upload.
The HTML page contains the URL of a pre-authenticated request to upload the file to a bucket.
