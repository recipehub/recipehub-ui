(function() {
    angular.module('recipehub')
        .controller('EditRecipeController', ['RecipeService', '$scope', '$routeParams', 'CommentService', 'RatingService', '$mdDialog', 'IngredientService', function recipeController($recipeService, $scope, $routeParams, $commentService, $ratingService, $mdDialog, $ingredientService) {

            var recipe = {
                ingredients: [{}, {}],
                steps: ['']
            };
            this.selectedIngredient = {};
            $scope.recipe = {};
            $scope.steps = [];
            var scope = $scope;
            $scope.newStep = ''

            $scope.results = {}


            $recipeService.getRecipe($routeParams.id)
                .then(function(response) {
                    console.log(response.data)
                    $scope.steps = response.data.steps
                    $scope.recipe = response.data
                    for (key in $scope.recipe.ingredients) {
                        if ($scope.recipe.ingredients[key]) {
                            $scope.recipe.ingredients[key]['selected'] = $scope.recipe.ingredients[key]
                            
                        }
                    }
                    console.log($scope.recipe.ingredients)
                })


            $ingredientService.getIngredients()
                .then(function (response) {
                    $scope.AllIngredients = response.data;
                });


            $scope.querySearch = function (query) {
                var results = query ? $scope.AllIngredients.filter( createFilterFor(query) ) : $scope.AllIngredients;
                return results;
            };
            $scope.addMoreIngredients = function () {
                $scope.recipe.ingredients.push({});
            };

            $scope.addStep = function () {
                $scope.steps.push($scope.newStep);

            };

            $scope.update = function () {
                var finalIngredients = {}
                for (key in $scope.recipe.ingredients) {
                    if ($scope.recipe.ingredients[key].selected) {
                        finalIngredients[$scope.recipe.ingredients[key].selected.id] = parseInt($scope.recipe.ingredients[key].amount)
                    }
                }
                var to_save = {
                    'title': $scope.recipe['title'],
                    'description': $scope.recipe['description'],
                    'ingredients': finalIngredients,
                    'message': $scope.recipe.message,
                    'steps': $scope.steps
                }
                console.log(to_save)
                $recipeService.updateRecipe($routeParams.id, to_save)
            };



            function createFilterFor(query) {
                var lowercaseQuery = angular.lowercase(query);

                return function filterFn(ingredient) {
                    return (angular.lowercase(ingredient.name).indexOf(lowercaseQuery) === 0);
                };

            }
        }]);

})();

