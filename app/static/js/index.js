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
                <li class="news-item" style="border: 2px solid #ccc; margin: 10px 0; border-radius: 5px; box-shadow: 2px 2px 2px #ccc;">
                <div style="border-bottom:1px solid black; padding-top: 10px; padding-bottom: 10px; padding-left: 5px;">
                    <h2 class="news-title">${item.title}</h2>
                </div>
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


function newsOpen(e) {
    const linkElement = e.target;
    const link = linkElement.getAttribute('data');
    linkElement.style.cursor = 'wait';
    linkElement.innerText = 'Loading...';
    const parentElement = linkElement.parentElement;
    getNews(link, (data) => {
        if (data.content.trim() == '') {
            parentElement.innerText = 'Premium article';
        }
        else { 
            parentElement.innerText = data.content;
        }
        // style for the content
        parentElement.style.padding = '10px';
        parentElement.style.textAlign = 'justify';
        parentElement.style.lineHeight = '1.5';
        parentElement.style.fontSize = '1.2em';
        parentElement.innerHTML += `<br><a href="${link}" target="_blank">Read Full Article</a>`;
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

document.addEventListener('DOMContentLoaded', () => { 

    document.getElementById("prev").addEventListener("click", function () {
        const pageno = parseInt(document.getElementById("page_number").innerText)
        if (pageno > 1) {
            getNewsList(pageno - 1);
            document.getElementById("page_number").innerText = pageno - 1;
            window.scrollTo(0, 0);
        }
    });

    document.getElementById("next").addEventListener("click", function () {
        const pageno = parseInt(document.getElementById("page_number").innerText)
        getNewsList(pageno + 1);
        document.getElementById("page_number").innerText = pageno + 1;
        window.scrollTo(0, 0);
    });

    getNewsList(1);


})