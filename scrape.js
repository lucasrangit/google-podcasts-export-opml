/**
 * Run the following code on https://podcasts.google.com/
 * @returns [ names ]
 */
function getGooglePodcastNames() {
    const scrollingCarousel = document.querySelector('scrolling-carousel span');
    const links = scrollingCarousel.getElementsByTagName('a');
    let podcasts = [];
    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        try {
            const img = link.querySelector('img');
            const name = img.alt;
            if (name === '') continue;
            podcasts.push(name);
        } catch (e) {
            const divs = link.getElementsByTagName("div");
            let currentDiv = divs[0];
            for (let i = 0; i < 3; i++) {
                currentDiv = currentDiv.getElementsByTagName("div")[0];
            }
            const name = currentDiv.innerText;
            if (name === '') continue;
            podcasts.push(name);
        }
    }
    return podcasts;
}
podcasts = getGooglePodcastNames();
console.log("Found ", Object.keys(podcasts).length, " podcasts in Subscriptions")
console.log(podcasts);
