function searchUsername() {
  getUsername = document.getElementById('getUsername')
  showUsername = document.getElementById('showUsername')
  var req = new XMLHttpRequest()
  var url = 'http://127.0.0.1:3000/api/users?username=' + getUsername.value
  req.open('GET', url, true)
  req.onload = function () {
    var data = JSON.parse(this.responseText)
    if (data.data == null) {
      showUsername.innerHTML = '(...找不到)'
    } else {
      showUsername.innerHTML = data.data.name
    }
  }
  req.send()
}
