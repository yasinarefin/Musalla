var initialzed_editors = 0; // variable to check if all editors are ready
const image_upload_handler = (blobInfo, progress) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    xhr.open('POST', `/create/${quiz_id}/upload/`);

    xhr.upload.onprogress = (e) => {
        progress(e.loaded / e.total * 100);
    };

    xhr.onload = () => {
        if (xhr.status === 403) {
            reject({ message: 'HTTP Error: ' + xhr.status, remove: true });
            return;
        }

        if (xhr.status < 200 || xhr.status >= 300) {
            reject('HTTP Error: ' + xhr.status);
            return;
        }

        const json = JSON.parse(xhr.responseText);

        if (!json || typeof json.location != 'string') {
            reject('Invalid JSON: ' + xhr.responseText);
            return;
        }

        resolve(json.location);
    };

    xhr.onerror = () => {
        reject('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
    };

    const formData = new FormData();
    formData.append('file', blobInfo.blob(), blobInfo.filename());
    formData.append('csrfmiddlewaretoken', csrf_token);
    xhr.send(formData);
});


function initTiny(){
    tinymce.init({
        selector: "textarea",
        automatic_uploads: true,
        images_upload_handler: image_upload_handler,
        plugins: [
            "insertdatetime",
            'image',
            'table',
        ],
        relative_urls : false,
        remove_script_host : true,
        setup: (editor) => {
            editor.on('init', () => {
               initialzed_editors++;
            });
        },
       // extended_valid_elements : "table[class=table table-bordered]",
        
    }

    )
}


initTiny();

// under development
function initWithTarget(element){
    tinymce.init({
        target: element,
        automatic_uploads: true,
        images_upload_handler: image_upload_handler,
        plugins: [
            "insertdatetime",
            'image',
            'table',
        ],
        relative_urls : false,
        remove_script_host : true,
        setup: (editor) => {
            editor.on('init', () => {
               initialzed_editors++;
            });
        },
        
        
    })
}


