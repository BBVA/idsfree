require 'nokogiri'

module Jekyll

  module TOCGenerator

    TOGGLE_HTML = '<li><a class="scrollto" href="#download-section">%1</a>%2</li>'
    TOC_CONTAINER_HTML = '<div class="doc-sidebar hidden-xs"><nav id="doc-nav"><ul id="doc-menu" class="nav doc-menu" data-spy="affix">%2</ul></nav></div>'
    HIDE_HTML = '<span class="toctoggle">[<a id="toctogglelink" class="internal" href="#">%1</a>]</span>'

    def toc_generate(html)
      # No Toc can be specified on every single page
      # For example the index page has no table of contents
      return html if (@context.environments.first["page"]["noToc"] || false)

      config = @context.registers[:site].config

      # Minimum number of items needed to show TOC, default 0 (0 means no minimum)
      min_items_to_show_toc = config["minItemsToShowToc"] || 0

      anchor_prefix = config["anchorPrefix"] || 'tocAnchor-'

      # better for traditional page seo, commonlly use h1 as title
      toc_top_tag = config["tocTopTag"] || 'h1'
      toc_top_tag = toc_top_tag.gsub(/h/, '').to_i

      toc_top_tag = 5 if toc_top_tag > 5

      toc_sec_tag = toc_top_tag + 1
      toc_top_tag = "h#{toc_top_tag}"
      toc_sec_tag = "h#{toc_sec_tag}"


      # Text labels
      contents_label     = config["contentsLabel"] || 'Contents'
      hide_label         = config["hideLabel"] || 'hide'
      # show_label       = config["showLabel"] || 'show' # unused
      show_toggle_button = config["showToggleButton"]

      toc_html = ''
      toc_level = 1
      toc_section = 1
      item_number = 1
      level_html = ''

      doc = Nokogiri::HTML(html)

      # Find H1 tag and all its H2 siblings until next H1
      doc.css(toc_top_tag).each do |tag|
        # TODO This XPATH expression can greatly improved
        ct    = tag.xpath("count(following-sibling::#{toc_top_tag})")
        sects = tag.xpath("following-sibling::#{toc_sec_tag}[count(following-sibling::#{toc_top_tag})=#{ct}]")

        level_html    = ''
        sub_section_html = ''
        inner_section = 0

        sects.each do |sect|
          inner_section += 1
          anchor_id = [
                        anchor_prefix, toc_level, '-', toc_section, '-',
                        inner_section
                      ].map(&:to_s).join ''

          sect['id'] = "#{anchor_id}"

          sub_section_html += create_sub_level_html(anchor_id,
                                                    sect.text)
        end

        level_html = '<ul class="nav doc-sub-menu">' + sub_section_html + '</ul>' if sub_section_html.length > 0

        anchor_id = anchor_prefix + toc_level.to_s + '-' + toc_section.to_s
        tag['id'] = "#{anchor_id}"

        toc_html += create_level_html(anchor_id,
                                      tag.text,
                                      level_html)

        toc_section += 1 + inner_section
        item_number += 1
      end

      # for convenience item_number starts from 1
      # so we decrement it to obtain the index count
      toc_index_count = item_number - 1

      return html unless toc_html.length > 0

      hide_html = ''
      hide_html = HIDE_HTML.gsub('%1', hide_label) if (show_toggle_button)

      if min_items_to_show_toc <= toc_index_count
        replaced_toggle_html = TOGGLE_HTML
        .gsub('%1', contents_label)
        .gsub('%2', hide_html)

        toc_table = TOC_CONTAINER_HTML
        .gsub('%1', replaced_toggle_html)
        .gsub('%2', toc_html)
      end

      '<div class="doc-content"><div class="content-inner">%1</div></div>%2'
      .gsub('%1', doc.css('body').children.to_xhtml)
      .gsub('%2', toc_table)
    end

    private

    def create_sub_level_html(anchor_id, tocText)
      #link = '<a href="#%1"><span class="tocnumber">%2</span> <span class="toctext">%3</span></a>%4'
      #link = '<li><a class="scrollto" href="#%1">%3</a></li>'
      link = '<li><a class="scrollto" href="#%1">%2</a></li>'
      .gsub('%1', anchor_id.to_s)
      .gsub('%2', tocText)
    end

    def create_level_html(anchor_id, tocText, subSection)
      #link = '<a href="#%1"><span class="tocnumber">%2</span> <span class="toctext">%3</span></a>%4'
      #link = '<li><a class="scrollto" href="#%1">%3</a></li>'
      link = '<li><a class="scrollto" href="#%1">%2</a>%3</li>'
      .gsub('%1', anchor_id.to_s)
      .gsub('%2', tocText)
      .gsub('%3', subSection)
    end

  end

end

Liquid::Template.register_filter(Jekyll::TOCGenerator)