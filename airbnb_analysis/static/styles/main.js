let ratingText = document.querySelector('#rating-user');
let rating = document.querySelector('.star-ratings.mutable');
let ratingTop = document.querySelector('.star-ratings.top.mutable');
let latestRatingStr = "0%";
let latestRating = 0; 
let realTimeRatingStr = "0%";
let realTimeRating = 0;
rating.addEventListener("mousemove", ratingMoveHandler);
rating.addEventListener("mouseout", ratingOutHandler);
rating.addEventListener("click", ratingClickHandler);
let ratingPosLeft = rating.offsetLeft;
// console.log("rating left:", ratingPosLeft);
function ratingMoveHandler(e) {
    realTimeRating = Math.round(((e.clientX - ratingPosLeft)/rating.clientWidth)*10);
    realTimeRatingStr = String(realTimeRating*10) + '%';
    // console.log("rating data:", realTimeRating);
    // ratingData = ratingData / rating.width
    ratingTop.style.width = realTimeRatingStr;
    // ratingText.innerHTML = "My Rating: " + realTimeRating;
    ratingText.value = realTimeRating;
}
function ratingOutHandler() {
    ratingTop.style.width = latestRatingStr;
    realTimeRating = latestRating;
    ratingText.value = latestRating;
    // ratingText.innerHTML = "My Rating: " + realTimeRating;
}
function ratingClickHandler() {
    latestRating = realTimeRating;
    latestRatingStr = String(latestRating*10) + '%';
}