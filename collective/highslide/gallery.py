from zope import interface
from zope import schema
from decimal import Decimal

from collective.configviews import ConfigurableBaseView

from collective.highslide.i18n import messageFactory as _
from collective.highslide import vocabulary
from zope.component._api import getUtility
from plone.registry.interfaces import IRegistry


class IHighSlideSettings(interface.Interface):
    """HighSlide display settings"""
    
    outlineType = schema.Choice(
        title=_(u"label_highslide_outlineType", default=u"Image outline type"),
        description=_(u"description_highslide_outlineType",
            default=u"The style of the border around the image. "
                    u"(*Highslide* display type)"
        ),
        default='drop-shadow',
        vocabulary=vocabulary.outlineType,
        )
    align = schema.Choice(title=_(u"Align"),
                    vocabulary=vocabulary.align,
                    default='center')

    transitions = schema.List(title=_(u'Transitions'),
                              value_type=schema.Choice(title=_(u'Transition'),
                                           vocabulary=vocabulary.transition),
                              default=['expand','crossfade'])
    fadeInOut = schema.Bool(title=_(u'Fade InOut'),
                            default=True)

    dimmingOpacity = schema.ASCIILine(title=_(u'Dimming opacity'),
                                    default='0.8')
    autoplay = schema.Bool(
        title=_(u"Auto play"),
        description=_(u"autoplay_description",
            default=u"Should this gallery automatically change images for the user?"
        ),
        default=True
    )
    
    transitionDuration = schema.Int(
        title=_(u"Transition Duration"),
        description=_(u"transitionDuration_description",
            default=u"The amount of time the change effect should "
                    u"take in miliseconds."
        ),
        default=500,
        required=True
    )
    
    interval = schema.Int(
        title=_(u"Interval"),
        description=_(u"interval_description",
            default=u"If slide show is timed, the delay sets "
                    u"how long before the next image is shown in miliseconds."
        ),
        default=5000,
        required=True
    )
    
    repeat = schema.Bool(title=_(u'Repeat'),
                         default=True)
    
    useControls = schema.Bool(title=_(u'Use controls'),
                              default=True)
    
    start_automatically = schema.Bool(title=_(u'Start automaticly'),
                                      default=True)
    
    start_index = schema.ASCIILine(title=_(u'Start index'),
                                   default='0')

JAVASCRIPT = """
hs.graphicsDir = '%(graphicsDir)s';
hs.align = '%(align)s';
hs.transitions = %(transitions)s;
hs.fadeInOut = %(fadeInOut)s;
hs.dimmingOpacity = %(dimmingOpacity)s;
hs.outlineType = '%(outlineType)s';
hs.wrapperClassName = %(wrapperClassName)s;
hs.captionEval = 'this.thumb.alt';
hs.marginBottom = 105; // make room for the thumbstrip and the controls
hs.numberPosition = 'caption';
hs.autoplay = %(autoplay)s;
hs.transitionDuration = %(transitionDuration)s;
hs.addSlideshow({
    interval: %(interval)s,
    repeat: %(repeat)s,
    useControls: %(useControls)s,
    fixedControls: 'fit',
    overlayOptions: {
        position: 'middle center',
        opacity: .7,
        hideOnMouseOut: true
    },
    thumbstrip: {
        position: 'bottom center',
        mode: 'horizontal',
        relativeTo: 'viewport'
    }
});

var highslide_auto_start = %(start_automatically)s;
var highslide_start_image_index = %(start_index)s;

(function($){
$(document).ready(function() {
    var images = $('a.highslide');
    if(images.length <= highslide_start_image_index){
        highslide_start_image_index = 0;
    }
    if(highslide_auto_start){
        $(images[highslide_start_image_index]).trigger('click');
    }
});
})(jQuery);
"""

class HighSlideGallery(ConfigurableBaseView):
    settings_schema = IHighSlideSettings
    jsvarname = 'highslide_settings'

    def portal_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name="plone_portal_state")
        return portal_state.portal_url()

    @property
    def settings(self):
        settings = super(HighSlideGallery, self).settings
        outlineType = settings['outlineType']

        settings['wrapperClassName'] = ''

        if outlineType=='drop-shadow':
            settings['wrapperClassName'] = 'dark borderless floating-caption'
            settings['outlineType'] = ''

        elif 'glossy-dark' in outlineType:
            settings['wrapperClassName'] = 'dark'

        if len(settings['wrapperClassName']) == 0:
            settings['wrapperClassName'] = 'null'
        else:
            settings['wrapperClassName'] = "'%s'" % settings['wrapperClassName']

        settings['graphicsDir'] = '++resource++collective.js.highslide/graphics/'

        return settings

    def settings_javascripts(self):
        settings = self.update_boolean_js(self.settings)
        return JAVASCRIPT%settings
    
    def update_boolean_js(self, settings):
        for i in ('fadeInOut','autoplay','useControls','start_automatically','repeat'):
            if settings[i]:
                settings[i]='true'
            else:
                settings[i]='false'
        return settings
