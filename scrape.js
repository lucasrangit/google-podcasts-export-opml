/**
 * Run the following code on https://podcasts.google.com/
 * @returns { name, url }
 */
function getGooglePodcastUrlFromFile() {
    // const links = document.querySelectorAll('scrolling-carousel span a');
    const scrollingCarousel = document.querySelector('scrolling-carousel span');
    const links = scrollingCarousel.getElementsByTagName('a');
    let podcasts = {};
    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        try {
            const img = link.querySelector('img');
            const name = img.alt;
            const url = link.href;
            podcasts[name] = url;
        } catch (e) {
            const divs = link.getElementsByTagName("div");
            let currentDiv = divs[0];
            for (let i = 0; i < 3; i++) {
                currentDiv = currentDiv.getElementsByTagName("div")[0];
            }
            possible_name = currentDiv.innerText;
            console.log("Failed to get URL for: ", possible_name );
        }
    }
    return podcasts;
}
podcasts = getGooglePodcastUrlFromFile();
console.log("Found ", Object.keys(podcasts).length, " podcasts in Subscriptions")
console.log(podcasts);
