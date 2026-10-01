/* ==========================================
   LakeNews Website
   JavaScript
========================================== */


/* ------------------------------------------
   NEWS DATA
------------------------------------------ */

const newsData = [

    {
        id: 1,

        title: "Sri Lanka sees new developments in technology and digital services",

        category: "Sri Lanka",

        date: "October 01, 2026",

        author: "LakeNews Team",

        image:
            "https://images.unsplash.com/photo-1523731407965-2430cd12f5e4?auto=format&fit=crop&w=1000&q=80",

        description:
            "New developments are creating more opportunities for digital services and technology across Sri Lanka.",

        content:
            "Technology continues to play an important role in Sri Lanka. New digital services, online platforms and technology projects are helping businesses and communities connect more easily."
    },


    {
        id: 2,

        title: "World leaders discuss technology, economy and global cooperation",

        category: "World",

        date: "October 01, 2026",

        author: "World Desk",

        image:
            "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1000&q=80",

        description:
            "International leaders are discussing major global economic and technology developments.",

        content:
            "Representatives from different countries continue discussions on international cooperation, economic development and emerging technologies."
    },


    {
        id: 3,

        title: "New artificial intelligence tools are changing the digital world",

        category: "Technology",

        date: "September 30, 2026",

        author: "Tech Desk",

        image:
            "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1000&q=80",

        description:
            "Artificial intelligence is becoming increasingly common in software, business and creative industries.",

        content:
            "AI technologies are developing rapidly. Businesses and developers are using artificial intelligence for automation, content creation, data analysis and many other applications."
    },


    {
        id: 4,

        title: "Football fans prepare for another exciting weekend",

        category: "Sports",

        date: "September 30, 2026",

        author: "Sports Desk",

        image:
            "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=1000&q=80",

        description:
            "Football supporters are preparing for another weekend of major matches and sporting events.",

        content:
            "Sports fans around the world are following upcoming matches, team news and player performances as another busy sporting weekend approaches."
    },


    {
        id: 5,

        title: "Colombo continues to grow as a modern business destination",

        category: "Sri Lanka",

        date: "September 29, 2026",

        author: "Business Desk",

        image:
            "https://images.unsplash.com/photo-1588258524675-cf54c8d2f4e4?auto=format&fit=crop&w=1000&q=80",

        description:
            "Business and development activities continue to shape Colombo's urban environment.",

        content:
            "Colombo remains an important commercial centre. New businesses, digital services and infrastructure developments continue to influence the city."
    },


    {
        id: 6,

        title: "Scientists explore new possibilities in space research",

        category: "World",

        date: "September 29, 2026",

        author: "Science Desk",

        image:
            "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1000&q=80",

        description:
            "Space research continues to provide new opportunities for scientific discovery.",

        content:
            "Researchers around the world continue studying space, planets and the wider universe using advanced scientific instruments and spacecraft."
    },


    {
        id: 7,

        title: "Smartphone technology continues to evolve rapidly",

        category: "Technology",

        date: "September 28, 2026",

        author: "Tech Desk",

        image:
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1000&q=80",

        description:
            "Modern smartphones are becoming more powerful with improved cameras, processors and AI features.",

        content:
            "Smartphone manufacturers continue to introduce new hardware and software features. Artificial intelligence, photography and battery technology remain important areas of development."
    },


    {
        id: 8,

        title: "Cricket continues to attract millions of fans worldwide",

        category: "Sports",

        date: "September 28, 2026",

        author: "Sports Desk",

        image:
            "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=1000&q=80",

        description:
            "Cricket remains one of the world's most popular sports.",

        content:
            "Cricket continues to attract large audiences around the world, with international tournaments and domestic competitions providing entertainment for millions of fans."
    },


    {
        id: 9,

        title: "Digital education creates new learning opportunities",

        category: "Technology",

        date: "September 27, 2026",

        author: "Education Desk",

        image:
            "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1000&q=80",

        description:
            "Online education platforms are providing new ways for students to learn.",

        content:
            "Digital learning platforms allow students to access educational resources from almost anywhere. Online courses, video lessons and interactive applications are becoming increasingly popular."
    }

];


/* ------------------------------------------
   VARIABLES
------------------------------------------ */

let currentCategory = "All";

let currentSearch = "";

let visibleNews = 6;


/* ------------------------------------------
   DOM ELEMENTS
------------------------------------------ */

const newsGrid =
    document.getElementById("newsGrid");

const searchInput =
    document.getElementById("searchInput");

const searchButton =
    document.getElementById("searchButton");

const noResults =
    document.getElementById("noResults");

const resultCount =
    document.getElementById("resultCount");

const loadMoreButton =
    document.getElementById("loadMoreButton");

const themeButton =
    document.getElementById("themeButton");

const mobileMenuButton =
    document.getElementById("mobileMenuButton");

const mobileNav =
    document.getElementById("mobileNav");

const articleModal =
    document.getElementById("articleModal");

const closeModal =
    document.getElementById("closeModal");


/* ------------------------------------------
   DISPLAY NEWS
------------------------------------------ */

function displayNews() {

    newsGrid.innerHTML = "";

    let filteredNews = getFilteredNews();

    let visibleItems =
        filteredNews.slice(0, visibleNews);


    resultCount.textContent =
        `Showing ${filteredNews.length} news ${filteredNews.length === 1 ? "story" : "stories"}`;


    if (visibleItems.length === 0) {

        noResults.classList.remove("hidden");

        loadMoreButton.style.display = "none";

        return;

    }


    noResults.classList.add("hidden");


    visibleItems.forEach(news => {

        const card =
            createNewsCard(news);

        newsGrid.appendChild(card);

    });


    if (visibleNews < filteredNews.length) {

        loadMoreButton.style.display = "inline-block";

    } else {

        loadMoreButton.style.display = "none";

    }

}


/* ------------------------------------------
   FILTER NEWS
------------------------------------------ */

function getFilteredNews() {

    return newsData.filter(news => {

        const categoryMatch =
            currentCategory === "All" ||
            news.category === currentCategory;


        const searchMatch =
            news.title.toLowerCase().includes(currentSearch) ||

            news.description.toLowerCase().includes(currentSearch) ||

            news.category.toLowerCase().includes(currentSearch);


        return categoryMatch && searchMatch;

    });

}


/* ------------------------------------------
   CREATE NEWS CARD
------------------------------------------ */

function createNewsCard(news) {

    const card =
        document.createElement("article");

    card.className = "news-card";


    card.innerHTML = `

        <div class="news-card-image">

            <img
                src="${news.image}"
                alt="${news.title}"
                loading="lazy"
            >

            <span class="news-category">
                ${news.category}
            </span>

        </div>


        <div class="news-card-body">

            <div class="news-meta">
                ${news.date} · ${news.author}
            </div>

            <h3>
                ${news.title}
            </h3>

            <p>
                ${news.description}
            </p>

            <button
                class="read-more"
                data-id="${news.id}"
            >
                Read Full Story →
            </button>

        </div>

    `;


    const readButton =
        card.querySelector(".read-more");


    readButton.addEventListener(
        "click",
        () => openArticle(news)
    );


    return card;

}


/* ------------------------------------------
   OPEN ARTICLE
------------------------------------------ */

function openArticle(news) {

    document.getElementById("modalImage").src =
        news.image;

    document.getElementById("modalCategory").textContent =
        news.category;

    document.getElementById("modalTitle").textContent =
        news.title;

    document.getElementById("modalDate").textContent =
        `${news.date} · ${news.author}`;

    document.getElementById("modalDescription").textContent =
        news.description;

    document.getElementById("modalContent").textContent =
        news.content;


    articleModal.classList.add("show");

    document.body.style.overflow = "hidden";

}


/* ------------------------------------------
   CLOSE ARTICLE
------------------------------------------ */

function closeArticle() {

    articleModal.classList.remove("show");

    document.body.style.overflow = "";

}


closeModal.addEventListener(
    "click",
    closeArticle
);


articleModal.addEventListener(
    "click",
    function(event) {

        if (event.target === articleModal) {

            closeArticle();

        }

    }
);


/* ------------------------------------------
   CATEGORY FILTER
------------------------------------------ */

function selectCategory(category) {

    currentCategory = category;

    visibleNews = 6;


    document
        .querySelectorAll(".category-button")
        .forEach(button => {

            button.classList.toggle(
                "active",
                button.dataset.category === category
            );

        });


    document
        .querySelectorAll(".nav-link")
        .forEach(link => {

            link.classList.toggle(
                "active",
                link.dataset.category === category
            );

        });


    displayNews();

    mobileNav.classList.remove("show");

}


/* ------------------------------------------
   CATEGORY BUTTONS
------------------------------------------ */

document
    .querySelectorAll("[data-category]")
    .forEach(element => {

        element.addEventListener(
            "click",
            function(event) {

                event.preventDefault();

                selectCategory(
                    this.dataset.category
                );

            }
        );

    });


/* ------------------------------------------
   SEARCH
------------------------------------------ */

function performSearch() {

    currentSearch =
        searchInput.value
            .trim()
            .toLowerCase();

    visibleNews = 6;

    displayNews();

}


searchInput.addEventListener(
    "input",
    performSearch
);


searchButton.addEventListener(
    "click",
    performSearch
);


/* ------------------------------------------
   LOAD MORE
------------------------------------------ */

loadMoreButton.addEventListener(
    "click",
    function() {

        visibleNews += 3;

        displayNews();

    }
);


/* ------------------------------------------
   DARK MODE
------------------------------------------ */

themeButton.addEventListener(
    "click",
    function() {

        document.body.classList.toggle("dark");


        const darkMode =
            document.body.classList.contains("dark");


        themeButton.textContent =
            darkMode ? "☀️" : "🌙";


        localStorage.setItem(
            "newsTheme",
            darkMode ? "dark" : "light"
        );

    }
);


/* ------------------------------------------
   LOAD SAVED THEME
------------------------------------------ */

const savedTheme =
    localStorage.getItem("newsTheme");


if (savedTheme === "dark") {

    document.body.classList.add("dark");

    themeButton.textContent = "☀️";

}


/* ------------------------------------------
   MOBILE MENU
------------------------------------------ */

mobileMenuButton.addEventListener(
    "click",
    function() {

        mobileNav.classList.toggle("show");

    }
);


/* ------------------------------------------
   NEWSLETTER
------------------------------------------ */

const newsletterForm =
    document.getElementById("newsletterForm");


newsletterForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();


        const email =
            document.getElementById("emailInput").value;


        alert(
            `Thank you! ${email} has been added to our newsletter.`
        );


        newsletterForm.reset();

    }
);


/* ------------------------------------------
   BREAKING NEWS
------------------------------------------ */

const breakingNews = [

    "Latest updates from Sri Lanka",

    "Technology continues to transform the world",

    "Global news and international developments",

    "Sports news and latest match updates",

    "Stay connected with NewsWave"

];


let breakingIndex = 0;


function updateBreakingNews() {

    document.getElementById(
        "breakingText"
    ).textContent =
        breakingNews[breakingIndex];


    breakingIndex =
        (breakingIndex + 1) %
        breakingNews.length;

}


setInterval(
    updateBreakingNews,
    6000
);


/* ------------------------------------------
   SCROLL TO NEWS
------------------------------------------ */

function scrollToNews() {

    document
        .getElementById("newsSection")
        .scrollIntoView({
            behavior: "smooth"
        });

}


/* ------------------------------------------
   CURRENT YEAR
------------------------------------------ */

document.getElementById("year").textContent =
    new Date().getFullYear();


/* ------------------------------------------
   ESC KEY CLOSE MODAL
------------------------------------------ */

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {

            closeArticle();

        }

    }
);


/* ------------------------------------------
   INITIAL LOAD
------------------------------------------ */

displayNews();