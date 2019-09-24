# fn-fileupload
function that provides a web page to upload a file to a bucket using a pre-authenticated request

A static HTML page displays a form requesting the presenter name and session ID.
Once submitted (POST), the fn-fileupload function is called. It returns another
HTML page to select the file to upload. The HTML page contains the URL of a
pre-authenticated request to upload the file to a bucket.
