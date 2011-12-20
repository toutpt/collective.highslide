from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.highslide.i18n import messageFactory as _

outlineType=SimpleVocabulary([
    SimpleTerm('rounded-white', 'rounded-white',
        _(u"label_highslide_outlineType_rounded_white",
                            default=u"Rounded White")),
    SimpleTerm('outer-glow', 'outer-glow',
        _(u"label_highslide_outlineType_outer_glow",
                            default=u"Outer Glow")),
    SimpleTerm('drop-shadow', 'drop-shadow',
        _(u"label_highslide_outlineType_drop_shadow",
                            default=u"Drop Shadow")),
    SimpleTerm('glossy-dark', 'glossy-dark',
        _(u"label_highslide_outlineType_glossy_dark",
                            default=u"Glossy Dark")
    )
])

align = SimpleVocabulary([
    SimpleTerm('center','center',
               _(u"Center")),
])

transition = SimpleVocabulary([
    SimpleTerm('expand','expand',_(u"Expand")),
    SimpleTerm('crossfade','crossfade',_(u"Crossfade")),
])
