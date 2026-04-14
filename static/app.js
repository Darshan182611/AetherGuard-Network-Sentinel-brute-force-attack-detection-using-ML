document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const logBody = document.getElementById('log-body');
    const totalEl = document.getElementById('total-packets');
    const normalEl = document.getElementById('normal-packets');
    const alertEl = document.getElementById('alert-packets');
    const threatRing = document.getElementById('threat-ring');
    const threatPercent = document.getElementById('threat-percent');
    const pulseIndicator = document.querySelector('.pulse-indicator');

    let total = 0;
    let normal = 0;
    let alerts = 0;
    let eventSource = null;

    startBtn.addEventListener('click', () => {
        if (startBtn.classList.contains('primary-btn')) {
            startStream();
        } else {
            stopStream();
        }
    });

    function startStream() {
        startBtn.textContent = "Stop Stream";
        startBtn.classList.replace('primary-btn', 'danger-btn');
        pulseIndicator.classList.add('active');

        logBody.innerHTML = '';

        eventSource = new EventSource('/stream');
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if(data.error) {
                console.error(data.error);
                appendRow(data.error, 'ERROR', '-', '0%');
                return;
            }

            total++;
            totalEl.innerText = total;

            if (data.status === 'ALERT') {
                alerts++;
                alertEl.innerText = alerts;
            } else {
                normal++;
                normalEl.innerText = normal;
            }

            const alertRatio = Math.round((alerts / total) * 100);
            threatPercent.innerText = alertRatio + '%';
            const color = alertRatio > 0 ? 'var(--danger)' : 'var(--success)';
            threatRing.style.background = `conic-gradient(${color} ${alertRatio}%, var(--glass-bg) ${alertRatio}%)`;

            appendRow(data.packet_id, data.details, data.status, data.confidence);
        };

        eventSource.onerror = function() {
            stopStream();
        };
    }

    function stopStream() {
        if(eventSource) {
            eventSource.close();
            eventSource = null;
        }
        startBtn.textContent = "Start Live Stream";
        startBtn.classList.replace('danger-btn', 'primary-btn');
        pulseIndicator.classList.remove('active');
    }

    function appendRow(id, details, status, confidence) {
        const tr = document.createElement('tr');
        tr.className = 'row-enter';
        
        const isAlert = status === 'ALERT';
        const badgeClass = isAlert ? 'badge-alert' : 'badge-normal';
        
        tr.innerHTML = `
            <td>#${id}</td>
            <td>${details}</td>
            <td><span class="badge ${badgeClass}">${status}</span></td>
            <td>${confidence}%</td>
        `;

        logBody.insertBefore(tr, logBody.firstChild);

        if (logBody.children.length > 50) {
            logBody.removeChild(logBody.lastChild);
        }
    }
});
