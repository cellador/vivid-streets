function getCookie(name) {
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
}

export default getCookie;