fetch('../../storage/data.json')
    .then(response => response.json())
    .then(data => {
        document.title = data.title;
        document.querySelector('meta[name="title"]').content = data.title;
        document.querySelector('meta[name="description"]').content = data.description;
        document.querySelector('meta[name="theme-color"]').content = data.color;
        document.querySelector('link[rel="icon"]').href = data.logo;
        document.querySelector('meta[property="og:site_name"]').content = data.author;
        document.querySelector('meta[property="og:url"]').content = data.url;
        document.querySelector('meta[property="og:title"]').content = data.title;
        document.querySelector('meta[property="og:description"]').content = data.description;
    })
    .catch(error => console.error(error));