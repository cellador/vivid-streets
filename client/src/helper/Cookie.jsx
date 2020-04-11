export function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const Cookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (Cookies.length === 0) {
    return null;
  }
  return decodeURIComponent(Cookies[0].split('=')[1]);
};

export function setCookie(name,value,days=-1) {  // ,days) {
  // 0 Days => delete, -1 => Session
  var expires = "Session";
  if (days >= 0) {
    if (days === 0) {
      expires = "Thu, 01 Jan 1970 00:00:01 GMT"
    }
    else {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
    }
  }
  // document.cookie = name + "=" + (value || "")  + expires + "; path=/";
  document.cookie = name + "=" + (value || "") + "; expires=" + expires + "; SameSite=strict; path=/";
};