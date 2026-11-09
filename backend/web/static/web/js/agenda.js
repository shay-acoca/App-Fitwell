function completeEvent(eventId) {
    const csrfToken = window.agendaConfig ? window.agendaConfig.csrfToken : '';
    
    fetch(`/${document.documentElement.lang}/agenda/complete/${eventId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update UI card
            const card = document.getElementById(`event-${eventId}`);
            if (card) {
                card.classList.add('bg-health/10', 'border-health/30', 'opacity-75');
                card.classList.remove('bg-surface', 'border-white/10', 'hover:border-primary/50');
                
                const title = card.querySelector('h4');
                if (title) title.classList.add('line-through', 'text-gray-500');
                
                const btn = card.querySelector('button[onclick^="completeEvent"]');
                if(btn) {
                    const badge = document.createElement('span');
                    // Replicate the exact classes from the template
                    badge.className = "text-health font-bold text-xs uppercase tracking-widest mr-2 font-mono border border-health/30 px-2 py-1 rounded bg-health/10";
                    // We assume 'Fait' is handled or we use the data message if available, 
                    // or better, pass the translation via config.
                    badge.innerText = window.agendaConfig.textDone || "Fait";
                    btn.parentNode.insertBefore(badge, btn);
                    btn.remove();
                }
            }
            
            // Show Energy Notification
            const notif = document.getElementById('xp-notification');
            const msg = document.getElementById('xp-message');
            if (notif && msg) {
                msg.innerText = data.message;
                notif.classList.remove('translate-y-20', 'opacity-0');
                
                setTimeout(() => {
                    notif.classList.add('translate-y-20', 'opacity-0');
                }, 4000);
            }
            
            // Optional: Update Navbar stats if possible, but page reload is simpler.
            setTimeout(() => location.reload(), 2000);
        }
    })
    .catch(error => console.error('Error:', error));
}
