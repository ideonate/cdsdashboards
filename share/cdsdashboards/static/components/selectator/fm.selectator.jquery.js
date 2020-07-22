/*
 Selectator jQuery Plugin
 A plugin for select elements
 version 3.2, Apr 9th, 2020
 by Ingi á Steinamørk

 The MIT License (MIT)

 Copyright (c) 2013 QODIO

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

(function($) {
	'use strict';
	$.selectator = function (_element, _options) {
		var defaults = {
			prefix: 'selectator_',
			height: 'auto',
			useDimmer: false,
			useSearch: true,
			showAllOptionsOnFocus: false,
			selectFirstOptionOnSearch: true,
			keepOpen: false,
			submitCallback: function () {},
			load: null,
			delay: 0,
			minSearchLength: 0,
			valueField: 'value',
			textField: 'text',
			searchFields: ['value', 'text'],
			placeholder: '',
			render: {
				selected_item: function (_item, escape) {
					var html = '';
					if (typeof _item.left !== 'undefined')
						html += '<div class="' + self.options.prefix + 'selected_item_left"><img src="' + escape(_item.left) + '" alt=""></div>';
					if (typeof _item.right !== 'undefined')
						html += '<div class="' + self.options.prefix + 'selected_item_right">' + escape(_item.right) + '</div>';
					html += '<div class="' + self.options.prefix + 'selected_item_title">' + ((typeof _item.text !== 'undefined') ? escape(_item.text) : '') + '</div>';
					if (typeof _item.subtitle !== 'undefined')
						html += '<div class="' + self.options.prefix + 'selected_item_subtitle">' + escape(_item.subtitle) + '</div>';
					html += '<div class="' + self.options.prefix + 'selected_item_remove">X</div>';
					return html;
				},
				option: function (_item, escape) {
					var html = '';
					if (typeof _item.left !== 'undefined')
						html += '<div class="' + self.options.prefix + 'option_left"><img src="' + escape(_item.left) + '" alt=""></div>';
					if (typeof _item.right !== 'undefined')
						html += '<div class="' + self.options.prefix + 'option_right">' + escape(_item.right) + '</div>';
					html += '<div class="' + self.options.prefix + 'option_title">' + ((typeof _item.text !== 'undefined') ? escape(_item.text) : '') + '</div>';
					if (typeof _item.subtitle !== 'undefined')
						html += '<div class="' + self.options.prefix + 'option_subtitle">' + escape(_item.subtitle) + '</div>';
					return html;
				}
			},
			labels: {
				search: 'Search...'
			}
		};

		var self = this;
		self.options = {};
		self.$source_element = $(_element);
		self.$container_element = null;
		self.$selecteditems_element = null;
		self.$input_element = null;
		self.$textlength_element = null;
		self.$options_element = null;
		self.$mask_element = null;
		self.usefilterResults = true;
		var is_single = self.$source_element.attr('multiple') === undefined;
		var is_multiple = !is_single;
		var using_remote_data = false;
		var has_visible_options = true;
		var delayTimer = null;
		var key = {
			backspace: 8,
			tab:       9,
			enter:    13,
			shift:    16,
			ctrl:     17,
			alt:      18,
			capslock: 20,
			escape:   27,
			pageup:   33,
			pagedown: 34,
			end:      35,
			home:     36,
			left:     37,
			up:       38,
			right:    39,
			down:     40
		};



		// INITIALIZE PLUGIN
		self.init = function () {
			self.options = $.extend(true, {}, defaults, _options);
			$.each(self.$source_element.data(), function (_key, _value) {
				if (_key.substring(0, 10) === 'selectator') {
					self.options[_key.substring(10, 11).toLowerCase() + _key.substring(11)] = _value;
				}
			});
			self.options.searchFields = typeof self.options.searchFields === 'string' ? self.options.searchFields.split(' ') : self.options.searchFields;
			self.$source_element.find('option').each(function () {
				$(this).data('value', this.value);
				$(this).data('text', this.text);
			});
			using_remote_data = self.options.load !== null;

			//// ================== CREATE ELEMENTS ================== ////
			// mask
			self.$mask_element = $('#' + self.options.prefix + 'mask');
			if (self.$mask_element.length === 0) {
				self.$mask_element = $(document.createElement('div'));
				self.$mask_element.attr('id', self.options.prefix + 'mask');
				self.$mask_element.attr('onclick', 'void(0)');
				self.$mask_element.on('click', function () {
					$(':focus').blur();
				});
				self.$mask_element.hide();
				$(document.body).prepend(self.$mask_element);
			}
			// source element
			self.$source_element.addClass('selectator');
			if (self.$source_element.attr('placeholder')) {
				self.options.placeholder = self.$source_element.attr('placeholder');
			}
			// container element
			self.$container_element = $(document.createElement('div'));
			if (self.$source_element.attr('id') !== undefined) {
				self.$container_element.attr('id', self.options.prefix + self.$source_element.attr('id'));
			}
			self.$container_element.addClass(self.options.prefix + 'element ' + (is_multiple ? 'multiple ' : 'single ') + 'options-hidden');
			if (!self.options.useSearch) {
				self.$container_element.addClass('disable_search');
			}
			self.$container_element.css({
				width: self.$source_element.css('width'),
				minHeight: self.$source_element.css('height'),
				padding: self.$source_element.css('padding'),
				'flex-grow': self.$source_element.css('flex-grow'),
				position: 'relative'
			});
			if (self.options.height === 'element') {
				self.$container_element.css({
					height: self.$source_element.outerHeight() + 'px'
				});
			}
			// textlength element
			self.$textlength_element = $(document.createElement('span'));
			self.$textlength_element.addClass(self.options.prefix + 'textlength');
			self.$textlength_element.css({
				position: 'absolute',
				visibility: 'hidden'
			});
			self.$container_element.append(self.$textlength_element);
			// selected items element
			self.$selecteditems_element = $(document.createElement('div'));
			self.$selecteditems_element.addClass(self.options.prefix + 'selected_items');
			self.$container_element.append(self.$selecteditems_element);
			// input element
			self.$input_element = $(document.createElement('input'));
			self.$input_element.addClass(self.options.prefix + 'input');
			self.$input_element.attr('tabindex', self.$source_element.attr('tabindex'));
			if (!self.options.useSearch) {
				self.$input_element.attr('readonly', true);
				self.$input_element.css({
					'width': '0px',
					'height': '0px',
					'overflow': 'hidden',
					'border': 0,
					'padding': 0,
					'position': 'absolute'
				});
			} else {
				if (is_single) {
					self.$input_element.attr('placeholder', self.options.labels.search);
				} else {
					if (self.options.placeholder !== '') {
						self.$input_element.attr('placeholder', self.options.placeholder);
					}
					self.$input_element.width(20);
				}
			}
			self.$input_element.attr('autocomplete', 'false');
			self.$container_element.append(self.$input_element);
			// options element
			self.$options_element = $(document.createElement('ul'));
			self.$options_element.addClass(self.options.prefix + 'options');

			self.$container_element.append(self.$options_element);
			self.$source_element.after(self.$container_element);
			self.$source_element.hide();


			//// ================== BIND ELEMENTS EVENTS ================== ////

			// source element
			self.$source_element.change(function () {
				renderSelectedItems();
			});

			// container element
			self.$container_element.on('focus', function () {
				self.$input_element.focus();
				self.$input_element.trigger('focus');
			});
			self.$container_element.on('mousedown', function (_e) {
				_e.preventDefault();
				self.$input_element.focus();
				self.$input_element.trigger('focus');
				// put text caret to end of search field
				if (self.$input_element[0].setSelectionRange) {
					self.$input_element[0].setSelectionRange(self.$input_element.val().length, self.$input_element.val().length);
				} else if (self.$input_element[0].createTextRange) {
					var range = self.$input_element[0].createTextRange();
					range.collapse(true);
					range.moveEnd('character', self.$input_element.val().length);
					range.moveStart('character', self.$input_element.val().length);
					range.select();
				}
			});
			self.$container_element.on('click', function () {
				self.$input_element.focus();
				self.$input_element.trigger('focus');
			});
			self.$container_element.on('dblclick', function () {
				self.$input_element.select();
				self.$input_element.trigger('focus');
			});

			// input element
			self.$input_element.on('keydown', function (_e) {
				var keyCode = _e.keyCode || _e.which;
				var $active = null;
				var $newActive = null;
				switch (keyCode) {
					case key.up:
						_e.preventDefault();
						showDropdown();
						$active = self.$options_element.find('.active');
						if ($active.length !== 0) {
							$newActive = $active.prevUntil('.' + self.options.prefix + 'option:visible').add($active).first().prev('.' + self.options.prefix + 'option:visible');
							$active.removeClass('active');
							$newActive.addClass('active');
						} else {
							self.$options_element.find('.' + self.options.prefix + 'option').filter(':visible').last().addClass('active');
						}
						scrollToActiveOption();
						break;
					case key.down:
						_e.preventDefault();
						showDropdown();
						$active = self.$options_element.find('.active');
						if ($active.length !== 0) {
							$newActive = $active.nextUntil('.' + self.options.prefix + 'option:visible').add($active).last().next('.' + self.options.prefix + 'option:visible');
							$active.removeClass('active');
							$newActive.addClass('active');
						} else {
							self.$options_element.find('.' + self.options.prefix + 'option').filter(':visible').first().addClass('active');
						}
						scrollToActiveOption();
						break;
					case key.escape:
						_e.preventDefault();
						break;
					case key.enter:
						_e.preventDefault();
						$active = self.$options_element.find('.active');
						if ($active.length !== 0) {
							selectOption();
						} else {
							if (self.$input_element.val() !== '') {
								self.options.submitCallback(self.$input_element.val());
							}
						}
						resizeSearchInput();
						break;
					case key.backspace:
						if (self.options.useSearch) {
							if (self.$input_element.val() === '' && is_multiple && self.$source_element.find('option:selected').length) {
								var lastSelectedItem = self.$source_element.find('option:selected').last()[0];
								lastSelectedItem.removeAttribute('selected');
								lastSelectedItem.selected = false;
								self.$source_element.trigger('change');
								renderSelectedItems();
							}
							resizeSearchInput();
						} else {
							_e.preventDefault();
						}
						break;
					default:
						resizeSearchInput();
						break;
				}
			});
			self.$input_element.on('keyup', function (_e) {
				_e.preventDefault();
				_e.stopPropagation();
				var keyCode = _e.which;
				switch (keyCode) {
					case key.escape:
						hideDropdown();
						break;
					case key.enter:
						if (!self.options.keepOpen) {
							hideDropdown();
						}
						break;
					case key.left:
					case key.right:
					case key.up:
					case key.down:
					case key.tab:
					case key.shift:
						// Prevent any action
						break;
					default:
						load();
						break;
				}
				if (self.$container_element.hasClass('options-hidden') && (keyCode === key.left || keyCode === key.right || keyCode === key.up || keyCode === key.down)) {
					showDropdown();
				}
				resizeSearchInput();
			});
			self.$input_element.on('focus', function () {
				self.$container_element.addClass('focused');
				if (is_single || self.options.showAllOptionsOnFocus || !self.options.useSearch) {
					if (!self.options.useSearch && using_remote_data) {
						load()
					}
					showDropdown();
				}
			});
			self.$input_element.on('blur', function () {
				self.$container_element.removeClass('focused');
				hideDropdown();
			});

			// bind selected item events
			self.$container_element.on('mousedown', '.' + self.options.prefix + 'selected_item_remove', function () {
				var source_item_element = $(this).closest('.' + self.options.prefix + 'selected_item').data('source_item_element');
				source_item_element.removeAttribute('selected');
				source_item_element.selected = false;
				if (is_single && self.$source_element.find('[value=""]').length) {
					var noValueOption = self.$source_element.find('[value=""]')[0];
					noValueOption.setAttribute('selected', '');
					noValueOption.selected = true;
				}
				self.$source_element.trigger('change');
				filterResults(self.usefilterResults);
				renderOptions();
				renderSelectedItems();
			});

			// bind option events
			self.$container_element.on('mouseover', '.' + self.options.prefix + 'option', function () {
				var $active = self.$options_element.find('.active');
				$active.removeClass('active');
				var $this = $(this);
				$this.addClass('active');
			});
			self.$container_element.on('mousedown', '.' + self.options.prefix + 'option', function (_e) {
				_e.preventDefault();
				_e.stopPropagation();
			});
			self.$container_element.on('mouseup', '.' + self.options.prefix + 'option', function () {
				selectOption();
			});
			self.$container_element.on('click', '.' + self.options.prefix + 'option', function (_e) {
				_e.stopPropagation();
				var $active = self.$options_element.find('.active');
				$active.removeClass('active');
				var $this = $(this);
				$this.addClass('active');
			});

			// Make elements accesible from options
			self.options.$source_element = self.$source_element;
			self.options.$container_element = self.$container_element;
			self.options.$selecteditems_element = self.$selecteditems_element;
			self.options.$input_element = self.$input_element;
			self.options.$textlength_element = self.$textlength_element;
			self.options.$options_element = self.$options_element;

			// Render
			renderOptions();
			renderSelectedItems();
			resizeSearchInput();
		};


		// RESIZE INPUT
		var resizeSearchInput = function () {
			if (is_multiple) {
				self.$textlength_element.text(self.$input_element.val() === '' && self.options.placeholder !== '' ? self.options.placeholder : self.$input_element.val());
				var width = self.$textlength_element.width() > (self.$container_element.width() - 30) ? (self.$container_element.width() - 30) : (self.$textlength_element.width() + 30);
				self.$input_element.css({ width: width + 'px' });
			}
		};


		// RENDER SELECTED ITEMS
		var renderSelectedItems = function () {
			self.$selecteditems_element.empty();
			self.$source_element.find('option').each(function () {
				var $option = $(this);
				if (this.selected) {
					var $item_element = $(document.createElement('div'));
					$item_element.data('source_item_element', this);
					$item_element.addClass(self.options.prefix + 'selected_item');
					$item_element.addClass(self.options.prefix + 'value_' + $option.val().replace(/\W/g, ''));
					if ($option.attr('class') !== undefined) {
						$item_element.addClass($option.attr('class'));
					}

					// fetch data
					var data = {
						value: this.value,
						text: this.text
					};
					$.each(this.attributes, function() {
						if(this.specified) {
							data[this.name.replace('data-', '')] = this.value;
						}
					});
					$.extend(data, $(this).data('item_data'));
					$item_element.append(self.options.render.selected_item(data, escape));
					if (is_single && (data[self.options.valueField] === '' || typeof data[self.options.valueField] === 'undefined' || self.$source_element.find('[value=""]').length === 0)) {
						$item_element.find('.' + self.options.prefix + 'selected_item_remove').remove();
					}
					self.$selecteditems_element.append($item_element);
				}
			});
			if (is_single) {
				if (self.options.placeholder !== '' && (self.$source_element.val() === '' || self.$source_element.val() === null)) {
					self.$selecteditems_element.empty();
					self.$selecteditems_element.append('<div class="' + self.options.prefix + 'placeholder">' + self.options.placeholder + '</div>');
				} else {
					self.$selecteditems_element.find('.' + self.options.prefix + 'placeholder').remove();
				}
			}
		};


		// RENDER OPTIONS
		var renderOptions = function () {
			self.$options_element.empty();
			var optionsArray = [];
			self.$source_element.children().each(function () {
				if ($(this).prop('tagName').toLowerCase() === 'optgroup') {
					var $group = $(this);
					if ($group.children('option').length !== 0) {
						var groupOptionsArray = [];
						$group.children('option').each(function () {
							groupOptionsArray.push({
								type: 'option',
								text: $(this).html(),
								element: this
							});
						});
						optionsArray.push({
							type: 'group',
							text: $group.attr('label'),
							options: groupOptionsArray,
							element: $group
						});
					}
				} else {
					optionsArray.push({
						type: 'option',
						text: $(this).html(),
						element: this
					});
				}
			});

			$(optionsArray).each(function () {
				if (this.type === 'group') {
					var $group_element = $(document.createElement('li'));
					$group_element.addClass(self.options.prefix + 'group');
					if ($(this.element).attr('class') !== undefined) {
						$group_element.addClass($(this.element).attr('class'));
					}
					$group_element.html($(this.element).attr('label'));
					self.$options_element.append($group_element);

					$(this.options).each(function () {
						var option = createOption.call(this.element, true);
						self.$options_element.append(option);
					});

				} else {
					var option = createOption.call(this.element, false);
					self.$options_element.append(option);
				}
			});
			filterResults(self.usefilterResults);
		};


		// CREATE RESULT OPTION
		var createOption = function (_isGroupOption) {
			// holder li
			var $option = $(document.createElement('li'));
			$option.data('source_option_element', this);
			$option.attr('onclick', 'void(0)');
			$option.addClass(self.options.prefix + 'option');
			$option.addClass(self.options.prefix + 'value_' + $(this).val().replace(/\W/g, ''));
			if (_isGroupOption) {
				$option.addClass(self.options.prefix + 'group_option');
			}
			if (this.selected) {
				$option.addClass('active');
			}
			// class
			if ($(this).attr('class') !== undefined) {
				$option.addClass($(this).attr('class'));
			}
			// fetch data
			var data = {
				value: this.value,
				text : this.text
			};
			$.each(this.attributes, function() {
				if(this.specified) {
					data[this.name.replace('data-', '')] = this.value;
				}
			});
			$.extend(data, $(this).data('item_data'));
			if (is_multiple && this.selected) {
				$option.hide();
			}

			$option.append(self.options.render.option(data, escape));

			return $option;
		};


		// LOAD SEARCH RESULTS (IF NEEDED)
		var load = function () {
			clearTimeout(delayTimer);
			delayTimer = setTimeout(function () {
				self.$container_element.addClass('loading');
				if (using_remote_data) {
					self.options.load(self.$input_element.val(), function (results, usefilterResults) {
						self.usefilterResults = typeof usefilterResults !== 'undefined' ? usefilterResults : false;
						self.$source_element.children('option').not(':selected').not('[value=""]').remove();
						if (typeof results !== 'undefined') {
							var selectedOptions = [];
							$.each(self.$source_element.children('option:selected'), function (_key, _option) {
								selectedOptions.push(_option.value);
							});
							if (is_single && self.$source_element.find('[value=""]').length === 0) {
								self.$source_element.prepend($('<option value="">&nbsp;</option>'));
							}
							if (self.$input_element.val().replace(/\s/g, '').length >= self.options.minSearchLength) {
								for (var i = 0; i < results.length; i++) {
									var result = results[i];
									if ($.inArray(result[self.options.valueField] + "", selectedOptions) === -1) {
										var $option = $('<option value="' + result[self.options.valueField] + '">' + result[self.options.textField] + '</option>');
										self.$source_element.append($option);
										$option.data('item_data', result);
									}
								}
							}
						}
						renderOptions();
						self.$container_element.removeClass('loading');
						filterResults(self.usefilterResults);
					});
				} else {
					self.$container_element.removeClass('loading');
					filterResults(self.usefilterResults);
				}
			}, self.options.delay);
		};


		// FILTER SEARCH RESULTS
		var filterResults = function (usefilterResults) {
			usefilterResults = typeof usefilterResults !== 'undefined' ? usefilterResults : false;
			// bool true if search field is below required length
			var searchIsBelowRequired = self.$input_element.val().replace(/\s/g, '').length < self.options.minSearchLength;
			// bool true if any options are visible
			has_visible_options = false;
			// get sanitized search text
			var searchFor = self.$input_element.val().toLowerCase();
			// iterate through the options
			self.$options_element.find('.' + self.options.prefix + 'option').each(function () {
				var $this = $(this);
				var source_option_element = $this.data('source_option_element');
				var $source_option_element = $(source_option_element);

				//  SHOW IF:
				// --------------------------------------------
				//  NOT using filter results
				//      AND option is NOT selected
				//  OR
				//      using filter results
				//      AND
				//          option is NOT selected
				//          OR single select
				//      AND
				//          use search
				//          AND
				//              searchtext is below required
				//              OR option text matches searchtext
				//              OR option value is empty
				//          OR NOT using search
				var match_found = false;
				$.each(self.options.searchFields, function (key, value) {
					if (typeof $source_option_element.data(value) !== 'undefined' && $source_option_element.data(value).toString().toLowerCase().indexOf(searchFor) !== -1) {
						match_found = true;
						return false;
					}
				});
				if (
					(!usefilterResults
						&& !source_option_element.selected
					)
					|| (usefilterResults
						&& (
							!source_option_element.selected
							|| is_single
						)
						&& (
							self.options.useSearch
							&& (
								searchIsBelowRequired
								|| match_found
								|| $source_option_element.val() === ''
							)
							|| !self.options.useSearch
						)
					)
				) {
					$this.show();
					has_visible_options = !has_visible_options ? true : has_visible_options;
				} else {
					$this.hide();
				}
			});
			// iterate through the groups
			self.$options_element.find('.' + self.options.prefix + 'group').each(function () {
				var $this = $(this);
				var has_visible_options = false;
				$this.nextUntil('.' + self.options.prefix + 'group').each(function () {
					var $option = $(this);
					if ($option.css('display') !== 'none') {
						has_visible_options = true;
						return false;
					}
				});
				// show if the group has any visible children
				if (has_visible_options) {
					$this.show();
				} else {
					$this.hide();
				}
			});
			showDropdown();
			if (is_multiple) {
				self.$options_element.find('.active').removeClass('active');
				if (!searchIsBelowRequired) {
					self.$options_element.find('.' + self.options.prefix + 'option').filter(':visible').first().addClass('active');
				}
			}
		};


		// SHOW OPTIONS AND MASK
		var showDropdown = function () {
			if (self.$input_element.is(':focus') && (has_visible_options || is_single ) && !(self.$options_element.is(':empty') && !self.options.useSearch)) {
				self.$container_element.removeClass('options-hidden').addClass('options-visible');
				self.$mask_element.show();
				if (self.options.useDimmer) {
					self.$mask_element.addClass(self.options.prefix + 'mask_dimmed');
				} else {
					self.$mask_element.removeClass(self.options.prefix + 'mask_dimmed');
				}
				setTimeout(function () {
					self.$options_element.css('top', (self.$container_element.outerHeight() + (is_multiple ? 0 : self.$input_element.outerHeight()) - 1) + 'px');
				}, 1);
				scrollToActiveOption();
			} else {
				hideDropdown();
			}
		};


		// HIDE OPTIONS AND MASK
		var hideDropdown = function () {
			self.$container_element.removeClass('options-visible').addClass('options-hidden');
			self.$mask_element.removeClass(self.options.prefix + 'mask_dimmed');
			self.$mask_element.hide();
		};


		// SCROLL TO ACTIVE OPTION IN OPTIONS LIST
		var scrollToActiveOption = function () {
			var $active_element = self.$options_element.find('.' + self.options.prefix + 'option.active');
			if ($active_element.length > 0) {
				self.$options_element.scrollTop(self.$options_element.scrollTop() + $active_element.position().top - self.$options_element.height()/2 + $active_element.height()/2);
			}
		};


		// SELECT ACTIVE OPTION
		var selectOption = function () {
			// select option
			if (is_single) {
				var lastSelectedItem = self.$source_element.find('option:selected').last()[0];
				lastSelectedItem.removeAttribute('selected');
				lastSelectedItem.selected = false;
			}
			var $active = self.$options_element.find('.active');
			$active.data('source_option_element').setAttribute('selected', '');
			$active.data('source_option_element').selected = true;
			self.$source_element.trigger('change');
			if (!self.options.keepOpen) {
				self.$input_element.val('');
			}
			filterResults(self.usefilterResults);
			renderSelectedItems();
			resizeSearchInput();
			if (using_remote_data && !self.options.keepOpen) {
				self.$source_element.children('option').not(':selected').not('[value=""]').remove();
				renderOptions();
				hideDropdown();
			}
			if (!self.options.keepOpen) {
				hideDropdown();
			}
		};


		// ESCAPE FUNCTION
		var escape = function(str) {
			return (str + '')
				.replace(/&/g, '&amp;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;')
				.replace(/"/g, '&quot;');
		};


		// REFRESH PLUGIN
		self.refresh = function () {
			renderSelectedItems();
		};


		// REMOVE PLUGIN AND REVERT SELECT ELEMENT TO ORIGINAL STATE
		self.destroy = function () {
			self.$container_element.remove();
			$.removeData(_element, 'selectator');
			self.$source_element.show();
			if ($('.' + self.options.prefix + 'element').length === 0) {
				self.$mask_element.remove();
			}
		};


		// Initialize plugin
		self.init();
	};

	// Initializer
	$.fn.selectator = function(_options) {
		var options = _options !== undefined ? _options : {};
		return this.each(function () {
			var $this = $(this);
			if (typeof(options) === 'object') {
				if ($this.data('selectator') === undefined) {
					var self = new $.selectator(this, options);
					$this.data('selectator', self);
				}
			} else if ($this.data('selectator')[options]) {
				$this.data('selectator')[options].apply(this, Array.prototype.slice.call(arguments, 1));
			} else {
				$.error('Method ' + options + ' does not exist in $.selectator');
			}
		});
	};
}(jQuery));

// Markup initializer
$(function () {
	'use strict';
	$('.selectator').each(function () {
		var $this = $(this);
		var options = {};
		$.each($this.data(), function (_key, _value) {
			if (_key.substring(0, 10) === 'selectator') {
				options[_key.substring(10, 11).toLowerCase() + _key.substring(11)] = _value;
			}
		});
		$this.selectator(options);
	});
});
