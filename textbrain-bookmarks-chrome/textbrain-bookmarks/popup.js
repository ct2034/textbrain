// Traverse the bookmark tree, and list the folder and nodes.
function getBookmarks() {
  chrome.bookmarks.getTree(
    function(bookmarkTreeNodes) {
      bookmarks = Array();
      traverseTree(bookmarkTreeNodes);
      document.getElementById("number").innerHTML = "Number of Bookmarks: " + bookmarks.length;
      var list = $('<ul>');
      var i;
      for (i = 0; i < bookmarks.length; i++) {
        list.append("<div>" + bookmarks[i].url + "</div>");
      }
      $('#bookmarks').append(list);
    });
}
function traverseTree(bookmarkNodes) {
  document.getElementById("number").innerHTML = "Number of Bookmarks: " + bookmarks.length;
  var list = $('<ul>');
  var i;
  for (i = 0; i < bookmarks.length; i++) {
    list.append("<div>" + bookmarks[i].title + "</div>");
  }
  $('#bookmarks').append(list);
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
  }
  else
  {
    bookmarks.push(node);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  getBookmarks();
});
