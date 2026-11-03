document.addEventListener('DOMContentLoaded', function () {
    const msgs = document.querySelectorAll('.mensagens .msg.success');
    msgs.forEach(function (m) {
        setTimeout(function () {
            m.style.display = 'none';
        }, 5000);
    });
});

(function () {
    var raiz = document.documentElement;
    var tam = 100, contraste = false;
    try {
        tam = parseInt(localStorage.getItem('acess-tam'), 10) || 100;
        contraste = localStorage.getItem('acess-contraste') === '1';
    } catch (e) {}

    function aplicar() {
        raiz.style.fontSize = tam + '%';
        raiz.classList.toggle('alto-contraste', contraste);
        var b = document.getElementById('acess-contraste');
        if (b) b.setAttribute('aria-pressed', contraste ? 'true' : 'false');
        try {
            localStorage.setItem('acess-tam', tam);
            localStorage.setItem('acess-contraste', contraste ? '1' : '0');
        } catch (e) {}
    }

    document.addEventListener('DOMContentLoaded', function () {
        var map = {
            'acess-aumentar': function () { tam = Math.min(tam + 10, 160); },
            'acess-diminuir': function () { tam = Math.max(tam - 10, 80); },
            'acess-contraste': function () { contraste = !contraste; },
            'acess-resetar': function () { tam = 100; contraste = false; }
        };
        Object.keys(map).forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.addEventListener('click', function () { map[id](); aplicar(); });
        });
        var ab = document.getElementById('acess-abrir'), pn = document.getElementById('acess-painel');
        if (ab && pn) {
            ab.addEventListener('click', function () {
                var abrir = pn.hidden;
                pn.hidden = !abrir;
                ab.setAttribute('aria-expanded', abrir ? 'true' : 'false');
            });
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape' && !pn.hidden) { pn.hidden = true; ab.setAttribute('aria-expanded', 'false'); ab.focus(); }
            });
        }
        aplicar();
    });
})();
