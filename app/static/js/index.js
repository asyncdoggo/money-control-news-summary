// display news list

async function getNewsList(page) {
    const response = await fetch('/news-list?page=' + page)
        .then(response => response.json())
        .then(data => {
            displayNewsList(data);
            // displayPagination(page);
        });
}

function displayNewsList(news) {
    const newsList = document.getElementById('news-list');
    newsList.innerHTML = '';
    news.forEach((item) => {
        const li = document.createElement('li');
        li.classList.add('news-list');
        li.innerHTML = `
                <li class="news-item">
                <h2 class="news-title">${item.title}</h2>
                <p>
                <button class="news_open" data="${item.link}" 
                onclick="newsOpen(event)"
                >Read More</button>
                </p>
            </li>
            `;
        newsList.appendChild(li);
    });
}


function displayPagination(page) {
    var pagination = document.getElementById('pagination');
    var paginationHtml = '';
    for (var i = 1; i <= page.total_pages; i++) {
        paginationHtml += '<li class="page-item"><a class="page-link" href="#" onclick="getNewsList(' + i + ')">' + i + '</a></li>';
    }
    pagination.innerHTML = paginationHtml;
}

function newsOpen(e) {
    const linkElement = e.target;
    const link = linkElement.getAttribute('data');
    linkElement.style.cursor = 'wait';
    linkElement.innerText = 'Loading...';
    const parentElement = linkElement.parentElement;
    getNews(link, (data) => {
        parentElement.innerText = data.content;
        // style for the content
        parentElement.style.padding = '10px';
        parentElement.style.textAlign = 'justify';
        parentElement.style.lineHeight = '1.5';
        parentElement.style.fontSize = '1.2em';
        parentElement.innerHTML += `<a href="${link}" target="_blank">Read Full</a>`;
    });
}

async function getNews(link, callback) {
    const response = await fetch('/news-content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ link: link })
    })
        .then(response => response.json())
        .then(data => {
            callback(data);
        });
}


getNewsList(1);