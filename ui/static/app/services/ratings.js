
(function(){

    var commentsPrefix = '/api/v1/comment/';

    angular.module('recipehub')
        .service('RatingService', ['$http', function recipeService($http) {
            this.makeComment = function (recipeId, text) {
                return $http.post(commentPrefix, {
                    params: {
                        recipe_id: recipeId,
                        text: text
                    }
                });
            };

            this.getCommentsForRecipe = function (recipeId) {
                return $http.get(commentsPrefix, {
                    params: {
                        recipe_id: recipeId
                    }
                });
            };

        }]);
})();
