odoo.define('web_digital_sign.web_digital_sign', function (require) {
    "use strict";

    var core = require('web.core');
    var BasicFields= require('web.basic_fields');
    var FormController = require('web.FormController');
    var Registry = require('web.field_registry');
    var utils = require('web.utils');
    var session = require('web.session');
    var field_utils = require('web.field_utils');

    var _t = core._t;
    var QWeb = core.qweb;
    
    // MIT http://rem.mit-license.org
    function trimCanvas(c) {
        var ctx = c.getContext('2d'),
            copy = document.createElement('canvas').getContext('2d'),
            pixels = ctx.getImageData(0, 0, c.width, c.height),
            l = pixels.data.length,
            i,
            bound = {
                top: null,
                left: null,
                right: null,
                bottom: null
            },
            x, y;
        
        // Iterate over every pixel to find the highest
        // and where it ends on every axis ()
        for (i = 0; i < l; i += 4) {
            if (pixels.data[i + 3] !== 0) {
                x = (i / 4) % c.width;
                y = ~~((i / 4) / c.width);

                if (bound.top === null) {
                    bound.top = y;
                }

                if (bound.left === null) {
                    bound.left = x;
                } else if (x < bound.left) {
                    bound.left = x;
                }

                if (bound.right === null) {
                    bound.right = x;
                } else if (bound.right < x) {
                    bound.right = x;
                }

                if (bound.bottom === null) {
                    bound.bottom = y;
                } else if (bound.bottom < y) {
                    bound.bottom = y;
                }
            }
        }
        
        // Calculate the height and width of the content
        var trimHeight = bound.bottom - bound.top,
            trimWidth = bound.right - bound.left,
            trimmed = ctx.getImageData(bound.left, bound.top, trimWidth, trimHeight);

        copy.canvas.width = trimWidth;
        copy.canvas.height = trimHeight;
        copy.putImageData(trimmed, 0, 0);

        // Return trimmed canvas
        return copy.canvas;
    }

    var FieldSignature = BasicFields.FieldBinaryImage.extend( {
        template: 'FieldSignature',
        events: _.extend({}, BasicFields.FieldBinaryImage.prototype.events, {
            'click .save_sign': '_on_save_sign',
            'click #sign_clean': '_on_clear_sign',
        }),
        jsLibs: ['/web_digital_sign/static/lib/jSignature/jSignatureCustom.js'],
        placeholder: "/web/static/src/img/placeholder.png",
        init: function (parent, name, record) {
            this._super.apply(this, arguments);
            this.sign_options = {
                'decor-color': '#D1D0CE',
                'color': '#000',
                'background-color': '#fff',
                'height': '150',
                'width': '550',
            };
            this.empty_sign = [];
        },
        start: function () {
            var self = this;
            this.$(".signature").jSignature("init", this.sign_options);
            this.$(".signature").attr( {
                "tabindex": "0",
                'height': "100",
            });
            this.$(".signature").bind('change',function(){
              var signature = this.$(".signature").jSignature("getData", 'image');
              console.log(signature);
            });
            this.empty_sign = this.$(".signature").jSignature("getData",'image');
            self._render();
            console.log(this.$(".signature"));
        },
        _on_clear_sign: function () {
            this.$(".signature > canvas").remove();
            this.$('> img').remove();
            this.$(".signature").attr("tabindex", "0");
            var sign_options = {
                'decor-color': '#D1D0CE',
                'color': '#000',
                'background-color': '#fff',
                'height': '150',
                'width': '550',
                'clear': true,
            };
            this.$(".signature").jSignature(sign_options);
            this.$(".signature").focus();
            this._setValue(false);
        },
        _on_save_sign: function (value_) {
            var self = this;
            this.$('> img').remove();
            var trimmedCanvas = trimCanvas(this.$(".signature > canvas"));
            var signature = trimmedCanvas.toDataURL("image/png");
            console.log(value_, signature);
            //var signature = this.$(".signature").jSignature("getData", 'image');
            //console.log(value_, signature);
            var is_empty = signature ?
                self.empty_sign[1] === signature[1] :
                false;
            if (!is_empty && typeof signature !== "undefined" && signature[1]) {
                this._setValue(signature[1]);
            }
        },
        _render: function () {
            var self = this;
            var url = this.placeholder;
            console.log(url);
            if (this.value && !utils.is_bin_size(this.value)) {
                url = 'data:image/png;base64,' + this.value;
            } else if (this.value) {
                url = session.url('/web/image', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.nodeOptions.preview_image || this.name,
                    unique:
                    field_utils.format.datetime(
                        this.recordData.__last_update).replace(/[^0-9]/g, ''),
                });
            } else {
                url = this.placeholder;
            }
            if (this.mode === "readonly") {
                var $img = $(QWeb.render("FieldBinaryImage-img", {
                    widget: self,
                    url: url,
                }));
                this.$('> img').remove();
                this.$(".signature").hide();
                this.$el.prepend($img);
                $img.on('error', function () {
                    self.on_clear();
                    $img.attr('src', self.placeholder);
                    self.do_warn(_t("Image"),
                        _t("Could not display the selected image."));
                });
            } else if (this.mode === "edit") {
                this.$('> img').remove();
                if (this.value) {
                    var field_name = this.nodeOptions.preview_image ?
                        this.nodeOptions.preview_image :
                        this.name;
                    self._rpc( {
                        model: this.model,
                        method: 'read',
                        args: [this.res_id, [field_name]],
                    }).then(function (data) {
                        if (data) {
                            var field_desc = _.values(_.pick(data[0],
                                field_name));
                            self.$(".signature").jSignature("clear");
                            self.$(".signature").jSignature("setData",
                                'data:image/png;base64,' + field_desc[0]);
                        }
                    });
                } else {
                    this.$('> img').remove();
                    this.$('.signature > canvas').remove();
                    var sign_options = {
                        'decor-color': '#D1D0CE',
                        'color': '#000',
                        'background-color': '#fff',
                        'height': '150',
                        'width': '550',
                    };
                    this.$(".signature").jSignature("init", sign_options);
                }
            } else if (this.mode === 'create') {
                this.$('> img').remove();
                this.$('> canvas').remove();
                if (!this.value) {
                    this.$(".signature").empty().jSignature("init", {
                        'decor-color': '#D1D0CE',
                        'color': '#000',
                        'background-color': '#fff',
                        'height': '150',
                        'width': '550',
                    });
                }
            }
        },
    });

    FormController.include( {
        saveRecord: function () {
            this.$('.save_sign').click();
            return this._super.apply(this, arguments);
        },
    });

    Registry.add('signature', FieldSignature);


});
