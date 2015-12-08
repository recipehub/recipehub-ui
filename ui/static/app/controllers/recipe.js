(function(){
    angular.module('recipehub')
        .controller('RecipeController', ['RecipeService', '$scope', '$routeParams', 'CommentService', 'RatingService', function recipeController($recipeService, $scope, $routeParams, $commentService, $ratingService) {

            var recipeId = $routeParams.id;
            var scope = $scope;

            $recipeService.getRecipe(recipeId)
                .then(function (response) {
                    $scope.recipe = response.data;
                });

            function putComments () {
                $commentService.getCommentsForRecipe(recipeId)
                    .then(function (response) {
                        $scope.comments = response.data;
                    });
            }

            $scope.makeComment = function () {
                var self = this;
                $commentService.makeComment(recipeId, this.newComment)
                    .then(function() {
                        putComments();
                        self.newComment = '';
                    });
            };

            putComments();
        }]);
})();
