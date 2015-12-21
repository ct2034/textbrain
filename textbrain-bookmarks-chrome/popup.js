// Traverse the bookmark tree, and list the folder and nodes.
$(function() {
  $('#pw').keypress(function (e) {
    if (e.which == 13) {
      getBookmarks();
      return false;
    }
  });
  chrome.storage.sync.get('pw', function(par) {
    if(par.pw) {
      $('#pw').val(par.pw);
    }  
  });
  chrome.storage.sync.get('url', function(par) {
    if(par.url) {
      $('#url').val(par.url);
    } 
  });  
  $('#result').innerHTML="A"
});

function getBookmarks() {
  chrome.bookmarks.getTree(
    function(bookmarkTreeNodes) {
      bookmarks = Array();
      traverseTree(bookmarkTreeNodes);
      document.getElementById("number").innerHTML = "Number of Bookmarks: " + bookmarks.length;
      var json_msg = {
        "pw": $('#pw').val(),
        "urls": []
      };
      var i;
      for (i = 0; i < bookmarks.length; i++) {
        json_msg["urls"][i] = bookmarks[i].url;
      }
      postRest($('#url').val(), JSON.stringify(json_msg));
      chrome.storage.sync.set({'pw': $('#pw').val()}, function() {});
      chrome.storage.sync.set({'url': $('#url').val()}, function() {});
    });
}

function traverseTree(bookmarkNodes) {
  var i;
  for (i = 0; i < bookmarkNodes.length; i++) {
    openNode(bookmarkNodes[i]);
  }
}

function openNode(node) {
  if (node.children) {
    var i;
    for (i = 0; i < node.children.length; i++) {
      openNode(node.children[i]);
    }
  } else {
    bookmarks.push(node);
  }
}

function postRest(url, json) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if(xmlhttp.responseText) {
      $('#result').innerHTML = xmlhttp.responseText;
    }
  }
  xmlhttp.open("POST", url, true)
  xmlhttp.send(json)
}

document.addEventListener('DOMContentLoaded', function() {
  // getBookmarks();
});