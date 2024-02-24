    function average_review(reviews) {
        let sum_reviews = 0;
        let count_reviews = 0;
        if(reviews.length > 0) {
            for (let review of reviews) {
                sum_reviews += Number(review[5]);
                count_reviews += 1;
            }
            return Math.round(sum_reviews / count_reviews);
        }
        else {
            return 0;
        }
    }

    function display_rating(average_rating){
        for(let i = 1; i < 6; i++){
            let element = document.getElementById(`rating_star_${i}`);
            if (average_rating > 0){
                element.setAttribute("src", "../static/yellow_star.png");
                average_rating = average_rating - 1;
            }
            else{
                element.setAttribute("src", "../static/grey_star.png");
            }
        }
    }