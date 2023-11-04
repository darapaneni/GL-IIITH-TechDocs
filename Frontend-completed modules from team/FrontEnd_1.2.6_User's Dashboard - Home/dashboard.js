
$(document).ready(function () {
  const links = document.querySelectorAll('.nav-link');
    
if (links.length) {
  links.forEach((link) => {
    link.addEventListener('click', (e) => {
      links.forEach((link) => {
          link.classList.remove('active');
      });
      e.preventDefault();
      link.classList.add('active');
    });
  });
}});
function getfilelist() {
alert("Hello I am going to get file list as you clicked on My documents button")
    try {
        $.ajax({
            headers: {'authToken': getUserToken()},
            contentType:"application/json; charset=utf-8",
            dataType: "json",
            type: 'GET',
            url: getApiUrl('filegetlist'),
            success: function(data){
              //alert(JSON.stringify(data));
              b1 = document.getElementById('new-doc');
              b2 = document.getElementById('share-doc');
              b3 = document.getElementById('archive-doc');
              b4 = document.getElementById('trash-doc');
              s1 = document.getElementById('searchfile');
              s2 = document.getElementById('searchtrash');
              t1 = document.getElementById('table1');
              t2 = document.getElementById('table2');

              b1.style.display='inline-block';
              b2.style.display='inline-block';
              b3.style.display='inline-block';
              b4.style.display='inline-block';
              s2.style.display='none';
              s1.style.display='inline-block';
              t2.style.display='none';
              t1.style.display='table';

              doc_data = JSON.stringify(data); 
              if(data){
                  var len = Object.keys(data.Documents).length;
                  var txt = "";
                  if(len > 0){
                    txt += 
                              '<thead><tr><th><input type="checkbox" id="selectall"></th><th scope="col">Title</th><th scope="col">Version</th><th scope="col">Last Modified</th>'+
                              '<th scope="col">Modified By</th><th scope="col">Actions</th></tr></thead><tbody></tbody>'
                      for(var i=0;i<len;i++){
                        var documentURL = getFrontEndUrl('latex-editor/'+data.Documents[i].DocId);
                  
                          if(data.Documents[i].DocName || data.Documents[i].Version || data.Documents[i].LastModifiedOn || data.Documents[i].LastModifiedBy){
                              txt+=                              
                              '<tr><td><input type="checkbox" class="case">'+"</td><td>"+
                              '<a href=\''+documentURL+' \'">'+data.Documents[i].DocName+'</a>'+"</td><td>"+
                              data.Documents[i].Version+ 
                              "</td><td>"+data.Documents[i].LastModifiedOn+"</td><td>"+data.Documents[i].LastModifiedBy + "</td>" +
                              '<td><div class="btn-group" role="group" aria-label="ROW BTNS">' +
                              
                              '<button type="button" id="rename" style="height: 25px; width: 25px; padding: 0px;" title="Rename"' +
                                'data-bs-toggle="modal" data-bs-target="#renameModal_'+data.Documents[i].DocId+'" class="btn btn-outline-dark">' +
                                '<i class="bi bi-input-cursor-text" style="font-size: 16px;"></i>' +
                              '</button>' +
                            // Rename modal
                              '<div class="modal fade" id="renameModal_'+data.Documents[i].DocId+'" tabindex="1" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
                              '<div class="modal-dialog">'+
                                '<div class="modal-content">'+
                                  '<div class="modal-header">'+
                                    '<h3 class="modal-title fs-5" id="exampleModalLabel">Rename file</h3>'+
                            
                                  '</div>'+
                            
                                  '<div class="modal-body">'+
                                    '<form class="input-group mb-3">'+
                                      '<input class="form-control" id="rename_'+data.Documents[i].DocId+'" type="text" placeholder="Enter new name" aria-label="default input example">'+
                                  '</form>'+
                                  '</div>'+
                                  '<div style="height: 100px; width: 100px; position: fixed;" id="rename-error-message" class="errorMessage"></div>'+
                                  '<div class="modal-footer">'+
                                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>'+
                                    '<button type="button" class="btn btn-primary" onclick="renamefile('+data.Documents[i].DocId+')">Change</button>'+
                                  '</div>'+
                                '</div>'+
                              '</div>'+
                            '</div>'+

                              '<button type="button" style="height: 25px; width: 25px; padding: 0px;" title="Share" data-docid="2" data-bs-toggle="modal"' + 
                              'data-bs-target="#shareModal_'+data.Documents[i].DocId+'" title="Share" class="btn btn-outline-dark">' + 
                              '<i class="bi bi-share" style="font-size: 16px;"></i>' +
                              '</button>' +

                              // Share modal
                              '<div class="modal fade" id="shareModal_'+data.Documents[i].DocId+'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
                                '<div class="modal-dialog">'+
                                  '<div class="modal-content">'+
                                    '<div class="modal-header">'+
                                      '<h1 class="modal-title fs-5" id="exampleModalLabel">Share Document</h1>'+
                                      '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                                    '</div>'+
                                    '<div class="modal-body">'+
                                      '<input type="hidden" name="docId" value="">'+
                                      '<div class="form-floating">'+
                                        '<input type="email" class="form-control" name="email" id="email-input_'+data.Documents[i].DocId+'" placeholder="email" required>'+
                                        '<label for="email-input">Email address</label>'+
                                      '</div>'+
                                      '<select id="sel_permissions_'+data.Documents[i].DocId+'" class="form-select form-select-lg mt-3" aria-label="Default select example">'+
                                        '<option value="read" selected="selected">Can View</option>'+
                                        '<option value="edit">Can Edit</option>'+
                                        '<option value="remove">Revoke Permissions</option>'+
                                      '</select>'+
                                    '</div>'+
                                    '<div class="modal-footer">'+
                                      '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'+
                                      '<button type="button" class="btn btn-primary" onclick="setpermissions('+data.Documents[i].DocId+')">Confirm</button>'+
                                    '</div>'+
                                  '</div>'+
                                '</div>'+
                              '</div>'+
                            '</div>'+


                              '<button type="button" id="download" style="height: 25px; width: 25px; padding: 0px;" title="Download"' +
                                'class="btn disabled">' +
                                '<i class="bi bi-download" style="font-size: 16px;"></i>' +
                              '</button>' +

                              '<button type="button" id="archive" style="height: 25px; width: 25px; padding: 0px;" title="Archive"' +
                                'class="btn disabled">' +
                                '<i class="bi bi-file-earmark-zip" style="font-size: 16px;"></i>' +
                              '</button>' +

                              '<button type="button" id="delete" onclick="trashalert('+data.Documents[i].DocId+')" style="height: 25px; width: 25px; padding: 0px;" title="Move to Trash"' +
                              ' class="btn btn-outline-dark">' +
                                '<i class="bi bi-trash3" style="font-size: 16px;"></i>' +
                              '</button>' +
                              
                            
                              "</div></td></tr>";
                          }
                      }
                      if(txt != ""){
                        //$("#table2").style.display='none';
                        //$("#table3").style.display='none';
                        $("#table1").html(txt);
        
                          
                          // Add multiple select / deselect functionality
                          $("#selectall").click(function () {
                            $('.case').attr('checked', this.checked);
                              })
                          
                      }
                  }
              }
          },
            error: function (data) {
                // in case of error we need to read response from data.responseJSON
                showAlert('#filelist-error-message', 'alert-danger', "", getResponseMessage(data));
            }
        });
    }
    catch (err) {
        console.log(err)
    }
}

window.onload = getfilelist();

//Search document
function filesearch() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchfile");
  filter = input.value.toUpperCase();
  table = document.getElementById("table1");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];

    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }}

  //Search trash
function trashsearch() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchtrash");
  filter = input.value.toUpperCase();
  table = document.getElementById("table2");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];

    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }}


// Share file
function setpermissions(DocId) {
  var e = document.getElementById("sel_permissions_"+DocId);
  selected_perm = e.options[e.selectedIndex].value;
  //alert(DocId);
  //alert($('#email-input_'+DocId).val());
  //alert(selected_perm);
  try{
    $.ajax({
      //headers: {'authToken': getUserToken()},
      contentType:"application/json; charset=utf-8",
      dataType: "json",
      data: JSON.stringify({
        DocId: DocId,
        share_email: $('#email-input_'+DocId).val(),
        permission_type: selected_perm
      }),
      type: 'POST',
      url: getApiUrl('set_permissions'),
      success: function(data){
        $('#shareModal_'+DocId).modal('hide');
        alert('File shared with' + ' ' +$('#email-input_'+DocId).val());
        getfilelist();
      },
      error: function (data) {
        // in case of error we need to read response from data.responseJSON
        alert(getResponseMessage(data));
        $('#shareModal_'+DocId).modal('hide');
        getfilelist();
      }
    });
}
catch (err) {
  console.log(err)
}
}

// Rename file
function renamefile(DocId) {
  try {
      $.ajax({
          //headers: {'authToken': getUserToken()},
          contentType:"application/json; charset=utf-8",
          dataType: "json",
          data: JSON.stringify({
            DocId: DocId,
            DocName: $('#rename_'+DocId).val()
          }),
          type: 'POST',
          url: getApiUrl('filerename'),
          success: function (data) {
            $('#renameModal_'+DocId).modal('hide');
            alert('File renamed successfully!');
            getfilelist();
          },
          error: function (data) {
              // in case of error we need to read response from data.responseJSON
              alert(getResponseMessage(data));
              $('#renameModal_'+DocId).modal('hide');
            getfilelist();
          }
      });
  }
  catch (err) {
      console.log(err)
  }
}

//Move to trash

function trashfile(DocId) {
  try {
    $.ajax({
       // headers: {'authToken': getUserToken(),},
        contentType:"application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify({
            DocId: DocId
        }),
        type: 'POST',
        url: getApiUrl('filetrash'),
        success: function (data) {
          alert("File moved to trash");
          getfilelist();
        },
        error: function (data) {
            // in case of error we need to read response from data.responseJSON
           alert(getResponseMessage(data));
        }
    });
}
catch (err) {
    console.log(err)
}
};

function trashalert(DocId) {
  let text;
  if (confirm("Do you want to delete this file?") == true) {
    trashfile(DocId);
  } else {
    
  }
}
          
//Get Trash List
function trashlist() {
alert("Hello I am going to get trash files as you clicked on trash button")
  try {
    $.ajax({
        headers: {'authToken': getUserToken()},
        contentType:"application/json; charset=utf-8",
        dataType: "json",
        type: 'GET',
        url: getApiUrl('getTrashList'),
        success: function(data){
          b1 = document.getElementById('new-doc');
          b2 = document.getElementById('share-doc');
          b3 = document.getElementById('archive-doc');
          b4 = document.getElementById('trash-doc');
          s1 = document.getElementById('searchfile');
          s2 = document.getElementById('searchtrash');
          t1 = document.getElementById('table1');
          t2 = document.getElementById('table2');
          
          b1.style.display='none';
          b2.style.display='none';
          b3.style.display='none';
          b4.style.display='none';
          s1.style.display='none';
          s2.style.display='inline-block';
          t1.style.display='none';
          t2.style.display='table';

          //$("#multi-retrieve").removeClass("hidden");
          //$("#multi-delete").removeClass("hidden");

          if(data){
            var len = Object.keys(data.Documents).length;
            var txt = "";
            
            if(len > 0){
              txt += 
                        '<thead><tr><th><input type="checkbox" id="selectalltrash"></th><th>Title</th><th>Actions</th></tr></thead><tbody></tbody>'
                for(var i=0;i<len;i++){
            
                    if(data.Documents[i].DocName){
                      
                        txt+=                              
                        '<tr><td><input type="checkbox" class="casetrash">'+"</td><td>"+data.Documents[i].DocName + "</td>"+
                        '<td><div class="btn-group" role="group" aria-label="ROW BTNS">' +
                        '<button type="button" id="retrieve" onclick="retrievealert('+data.Documents[i].DocId+')"  style="height: 25px; width: 25px; padding: 0px;" title="Retrieve"' +
                          'class="btn btn-outline-dark">' +
                          '<i class="bi bi-arrow-90deg-right" style="font-size: 16px;"></i>' +
                        '</button>' +

                        '<button type="button" id="delete" onclick="deletealert('+data.Documents[i].DocId+')" style="height: 25px; width: 25px; padding: 0px;" title="Delete permanently"' +
                          'data-bs-toggle="modal" data-bs-target="#delModal" class="btn btn-outline-dark">' +
                          '<i class="bi bi-x-circle" style="font-size: 16px;"></i>' +
                        '</button>' +
                      
                        "</div></td></tr>";
                    }
                }
                if(txt != ""){
                  //$("#table1").style.display='none';
                  //$("#table3").style.display='none';
                  $("#table2").html(txt);
                    
                    // Add multiple select / deselect functionality
                    $("#selectalltrash").click(function () {
                      $('.casetrash').attr('checked', this.checked);
                        })
                    
                }
            }
        }
        },
        error: function (data) {
            // in case of error we need to read response from data.responseJSON
            showAlert('#filelist-error-message', 'alert-danger', "", getResponseMessage(data));
        }
    });
}
catch (err) {
    console.log(err)
}
}

function retrievefile(DocId) {
  try {
      $.ajax({
          //headers: {'authToken': getUserToken()},
          contentType:"application/json; charset=utf-8",
          dataType: "json",
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
              // in case of error we need to read response from data.responseJSON
              showAlert('#rename-error-message', 'alert-danger', "", getResponseMessage(data));
          }
      });
  }
  catch (err) {
      console.log(err)
  }
}

function retrievealert(DocId) {
  let text;
  if (confirm("Do you want to retrieve this file?") == true) {
    retrievefile(DocId);
  } else {
    
  }
}

function deletefile(DocId) {
  try {
      $.ajax({
          //headers: {'authToken': getUserToken()},
          contentType:"application/json; charset=utf-8",
          dataType: "json",
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
              // in case of error we need to read response from data.responseJSON
              showAlert('#rename-error-message', 'alert-danger', "", getResponseMessage(data));
          }
      });
  }
  catch (err) {
      console.log(err)
  }
}

function deletealert(DocId) {
  let text;
  if (confirm("Do you want to permanently delete this file?") == true) {
    deletefile(DocId);
  } else {
    
  }
}

function sharedlist() {
alert("Hello I am going to get shared files list as you clicked on shared by others button")
  try {
    $.ajax({
        headers: {'authToken': getUserToken()},
        contentType:"application/json; charset=utf-8",
        dataType: "json",
        type: 'GET',
        url: getApiUrl('getsharedlist'),
        success: function(data){
          //alert(JSON.stringify(data));

          b1 = document.getElementById('new-doc');
          b2 = document.getElementById('share-doc');
          b3 = document.getElementById('archive-doc');
          b4 = document.getElementById('trash-doc');
          s1 = document.getElementById('searchfile');
          s2 = document.getElementById('searchtrash');
          t1 = document.getElementById('table1');
          t2 = document.getElementById('table2');
          
          b1.style.display='inline-block';
          b2.style.display='inline-block';
          b3.style.display='inline-block';
          b4.style.display='inline-block';
          s2.style.display='none';
          s1.style.display='inline-block';
          t2.style.display='none';
          t1.style.display='table';

          //$("#multi-retrieve").removeClass("hidden");
          //$("#multi-delete").removeClass("hidden");

          if(data){
            var len = Object.keys(data.Documents).length;
            var txt = "";
            
            if(len > 0){
              txt += 
              '<thead><tr><th><input type="checkbox" id="selectall"></th><th scope="col">Title</th><th scope="col">Version</th><th scope="col">Last Modified</th>'+
              '<th scope="col">Modified By</th><th scope="col">Actions</th></tr></thead><tbody></tbody>'
      for(var i=0;i<len;i++){
        var documentURL = getFrontEndUrl('latex-editor/'+data.Documents[i].DocId);
  
          if(data.Documents[i].DocName || data.Documents[i].Version || data.Documents[i].LastModifiedOn || data.Documents[i].LastModifiedBy){
              txt+=                              
              '<tr><td><input type="checkbox" class="case">'+"</td><td>"+
              '<a href=\''+documentURL+' \'">'+data.Documents[i].DocName+'</a>'+"</td><td>"+
              data.Documents[i].Version+ 
              "</td><td>"+data.Documents[i].LastModifiedOn+"</td><td>"+data.Documents[i].LastModifiedBy + "</td>" +
              '<td><div class="btn-group" role="group" aria-label="ROW BTNS">' +
              
              '<button type="button" id="rename" style="height: 25px; width: 25px; padding: 0px;" title="Rename"' +
                'data-bs-toggle="modal" data-bs-target="#renameModal_'+data.Documents[i].DocId+'" class="btn btn-outline-dark">' +
                '<i class="bi bi-input-cursor-text" style="font-size: 16px;"></i>' +
              '</button>' +
            // Rename modal
              '<div class="modal fade" id="renameModal_'+data.Documents[i].DocId+'" tabindex="1" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
              '<div class="modal-dialog">'+
                '<div class="modal-content">'+
                  '<div class="modal-header">'+
                    '<h3 class="modal-title fs-5" id="exampleModalLabel">Rename file</h3>'+
            
                  '</div>'+
            
                  '<div class="modal-body">'+
                    '<form class="input-group mb-3">'+
                      '<input class="form-control" id="rename_'+data.Documents[i].DocId+'" type="text" placeholder="Enter new name" aria-label="default input example">'+
                  '</form>'+
                  '</div>'+
                  '<div style="height: 100px; width: 100px; position: fixed;" id="rename-error-message" class="errorMessage"></div>'+
                  '<div class="modal-footer">'+
                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>'+
                    '<button type="button" class="btn btn-primary" onclick="renamefile('+data.Documents[i].DocId+')">Change</button>'+
                  '</div>'+
                '</div>'+
              '</div>'+
            '</div>'+

              '<button type="button" style="height: 25px; width: 25px; padding: 0px;" title="Share" data-docid="2" data-bs-toggle="modal"' + 
              'data-bs-target="#shareModal_'+data.Documents[i].DocId+'" title="Share" class="btn btn-outline-dark">' + 
              '<i class="bi bi-share" style="font-size: 16px;"></i>' +
              '</button>' +

              // Share modal
              '<div class="modal fade" id="shareModal_'+data.Documents[i].DocId+'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
                '<div class="modal-dialog">'+
                  '<div class="modal-content">'+
                    '<div class="modal-header">'+
                      '<h1 class="modal-title fs-5" id="exampleModalLabel">Share Document</h1>'+
                      '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                    '</div>'+
                    '<div class="modal-body">'+
                      '<input type="hidden" name="docId" value="">'+
                      '<div class="form-floating">'+
                        '<input type="email" class="form-control" name="email" id="email-input_'+data.Documents[i].DocId+'" placeholder="email" required>'+
                        '<label for="email-input">Email address</label>'+
                      '</div>'+
                      '<select id="sel_permissions_'+data.Documents[i].DocId+'" class="form-select form-select-lg mt-3" aria-label="Default select example">'+
                        '<option value="read" selected="selected">Can View</option>'+
                        '<option value="edit">Can Edit</option>'+
                        '<option value="remove">Revoke Permissions</option>'+
                      '</select>'+
                    '</div>'+
                    '<div class="modal-footer">'+
                      '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'+
                      '<button type="button" class="btn btn-primary" onclick="permissions('+data.Documents[i].DocId+')">Confirm</button>'+
                    '</div>'+
                  '</div>'+
                '</div>'+
              '</div>'+
            '</div>'+


              '<button type="button" id="download" style="height: 25px; width: 25px; padding: 0px;" title="Download"' +
                'class="btn disabled">' +
                '<i class="bi bi-download" style="font-size: 16px;"></i>' +
              '</button>' +

              '<button type="button" id="archive" style="height: 25px; width: 25px; padding: 0px;" title="Archive"' +
                'class="btn disabled">' +
                '<i class="bi bi-file-earmark-zip" style="font-size: 16px;"></i>' +
              '</button>' +

              '<button type="button" id="delete" onclick="trashalert('+data.Documents[i].DocId+')" style="height: 25px; width: 25px; padding: 0px;" title="Move to Trash"' +
              ' class="btn btn-outline-dark">' +
                '<i class="bi bi-trash3" style="font-size: 16px;"></i>' +
              '</button>' +
              
            
              "</div></td></tr>";
          }
      }
      if(txt != ""){
                    //$("#table1").addClass('hidden');
                    //$("#table2").style.display='none';
                    $("#table1").html(txt)
                    
                }
            }
        }
        },
        error: function (data) {
            // in case of error we need to read response from data.responseJSON
            showAlert('#filelist-error-message', 'alert-danger', "", getResponseMessage(data));
        }
    });
}
catch (err) {
    console.log(err)
}
}
