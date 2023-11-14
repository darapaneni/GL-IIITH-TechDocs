$(document).ready(function () {
    // Function to get the list of files in the trash
    function trashlist() {
      try {
        $.ajax({
          headers: { 'authToken': getUserToken() },
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          type: 'GET',
          url: getApiUrl('getTrashList'),
          success: function (data) {
            b1 = document.getElementById('new-doc');
            b2 = document.getElementById('share-doc');
            b3 = document.getElementById('archive-doc');
            b4 = document.getElementById('trash-doc');
            s1 = document.getElementById('searchfile');
            s2 = document.getElementById('searchtrash');
            t1 = document.getElementById('table1');
            t2 = document.getElementById('table2');
  
            b1.style.display = 'none';
            b2.style.display = 'none';
            b3.style.display = 'none';
            b4.style display = 'none';
            s1.style.display = 'none';
            s2.style.display = 'inline-block';
            t1.style.display = 'none';
            t2.style.display = 'table';
  
            if (data) {
              var len = Object.keys(data.Documents).length;
              var txt = '';
  
              if (len > 0) {
                txt +=
                  '<thead><tr><th><input type="checkbox" id="selectalltrash"></th><th>Title</th><th>Actions</th></tr></thead><tbody></tbody>';
                for (var i = 0; i < len; i++) {
                  if (data.Documents[i].DocName) {
                    txt +=
                      '<tr><td><input type="checkbox" class="casetrash"></td><td>' +
                      data.Documents[i].DocName +
                      '</td>' +
                      '<td><div class="btn-group" role="group" aria-label="ROW BTNS">' +
                      '<button type="button" id="retrieve" onclick="retrievealert(' +
                      data.Documents[i].DocId +
                      ')"  style="height: 25px; width: 25px; padding: 0px;" title="Retrieve"' +
                      'class="btn btn-outline-dark">' +
                      '<i class="bi bi-arrow-90deg-right" style="font-size: 16px;"></i>' +
                      '</button>' +
                      '<button type="button" id="delete" onclick="deletealert(' +
                      data.Documents[i].DocId +
                      ')" style="height: 25px; width: 25px; padding: 0px;" title="Delete permanently"' +
                      'data-bs-toggle="modal" data-bs-target="#delModal" class="btn btn-outline-dark">' +
                      '<i class="bi bi-x-circle" style="font-size: 16px;"></i>' +
                      '</button>' +
                      '</div></td></tr>';
                  }
                }
                if (txt != '') {
                  $("#table2").html(txt);
  
                  // Add multiple select / deselect functionality
                  $("#selectalltrash").click(function () {
                    $('.casetrash').attr('checked', this.checked);
                  });
                }
              }
            }
          },
          error: function (data) {
            // Handle the error response
            showAlert('#filelist-error-message', 'alert-danger', '', getResponseMessage(data));
          },
        });
      } catch (err) {
        console.log(err);
      }
    }
  
    // Function to retrieve a file from the trash
    function retrievefile(DocId) {
      try {
        $.ajax({
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          data: JSON.stringify({
            DocId: DocId,
          }),
          type: 'POST',
          url: getApiUrl('fileretrive'),
          success: function (data) {
            alert('File retrieved successfully');
            trashlist();
          },
          error: function (data) {
            showAlert('#rename-error-message', 'alert-danger', '', getResponseMessage(data));
          },
        });
      } catch (err) {
        console.log(err);
      }
    }
  
    // Function to display a confirmation dialog and then call the retrievefile function
    function retrievealert(DocId) {
      if (confirm('Do you want to retrieve this file?') == true) {
        retrievefile(DocId);
      } else {
        // Handle the cancel action
      }
    }
  
    // Function to permanently delete a file from the trash
    function deletefile(DocId) {
      try {
        $.ajax({
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          data: JSON.stringify({
            DocId: DocId,
          }),
          type: 'POST',
          url: getApiUrl('filedelete'),
          success: function (data) {
            alert('File deleted permanently');
            trashlist();
          },
          error: function (data) {
            showAlert('#rename-error-message', 'alert-danger', '', getResponseMessage(data));
          },
        });
      } catch (err) {
        console.log(err);
      }
    }
  
    // Function to display a confirmation dialog and then call the deletefile function
    function deletealert(DocId) {
      if (confirm('Do you want to permanently delete this file?') == true) {
        deletefile(DocId);
      } else {
        // Handle the cancel action
      }
    }
  
    // Load the list of files in the trash on page load
    trashlist();
  });
  