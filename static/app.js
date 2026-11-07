const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
if (menuBtn && sidebar) {
  menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  sidebar.querySelectorAll('a').forEach(link => link.addEventListener('click', () => sidebar.classList.remove('open')));
}
const search = document.getElementById('searchInput');
if (search) {
  search.addEventListener('input', () => {
    const q = search.value.toLocaleLowerCase('fr').trim();
    document.querySelectorAll('.record.searchable').forEach(item => {
      item.style.display = item.innerText.toLocaleLowerCase('fr').includes(q) ? '' : 'none';
    });
  });
}
document.querySelectorAll('input[type="date"]').forEach(input => {
  input.addEventListener('focus', () => input.showPicker && input.showPicker());
});
