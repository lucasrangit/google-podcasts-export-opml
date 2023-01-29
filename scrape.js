/**
 * Run the following code on https://podcasts.google.com/
 * @returns { name, url }
 */
function getGooglePodcastUrlFromFile() {
    const scrollingCarousel = document.querySelector('scrolling-carousel span');
    const links = scrollingCarousel.getElementsByTagName('a');
    var podcasts = {};
    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        try {
            const img = link.getElementsByTagName('img')[0];
            if (!img) {
                continue;
            }
            const name = img.alt;
            if (name === '') {
                continue;
            }
            const url = link.href;
            if (url === '') {
                continue;
            }
            podcasts[name] = url;
        } catch (e) {
            console.log(e);
            const divs = link.getElementsByTagName("div");
            let currentDiv = divs[0];
            for (let i = 0; i < 3; i++) {
                currentDiv = currentDiv.getElementsByTagName("div")[0];
            }
            maybe_name = currentDiv.innerText;
            console.log("Failed to get URL for: ", maybe_name );
        }
    }
    return podcasts;
}
console.log(getGooglePodcastUrlFromFile());
