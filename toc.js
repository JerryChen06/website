document.addEventListener('DOMContentLoaded', function() {
    // grab every <h1> or <h2> in the about-section that has an id
    const sections = Array.from(
        document.querySelectorAll('.about-section h1[id], .about-section h2[id]')
    );
    const links = Array.from(
        document.querySelectorAll('.about-table-contents a')
    );

    function onScroll() {
        const scrollPos = window.scrollY + 80; // offset for your navbar height
        let currentId = sections[0].id;

        for (let sec of sections) {
            if (sec.offsetTop <= scrollPos) {
                currentId = sec.id;
            }
        }

        links.forEach(a => {
            a.classList.toggle(
                'active',
                a.getAttribute('href') === '#' + currentId
            );
        });
    }

    window.addEventListener('scroll', onScroll);
    onScroll(); // highlight on load
});