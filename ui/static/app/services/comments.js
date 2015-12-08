(function(){

    var commentPrefix = '/api/v1/comment/';

    angular.module('recipehub')
        .service('CommentService', ['$http', function recipeService($http) {
            this.makeComment = function (recipeId, commentText) {
                return $http.post(commentPrefix, {
                    recipe_id: recipeId,
                    text: commentText
                });
            };

            this.getCommentsForRecipe = function (recipeId) {
                return $http.get(commentPrefix, {
                    params: {
                        recipe_id: recipeId
                    }
                });
            };

        }]);
})();
