#!/usr/bin/perl
# use strict;
use warnings;
use Data::Dumper;

require 'docker-lib.pl';

ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);

@tabs = ( [ 'info', $text{'tab_info'} ],
            [ 'containers', $text{'tab_containers'} ] );

print ui_tabs_start(\@tabs, 'info', 'containers', 1);

# INFO TAB
print ui_tabs_start_tab('mode', 'info');
my($status_fail, $status) = get_status();
if ($status_fail) {
    print ui_alert_box($status_fail, 'danger');
} else {
    print circular_grid($status);  # Ugly recursive output
}
print ui_tabs_end_tab('mode', 'info');

# CONTAINERS TAB
print ui_tabs_start_tab('mode', 'containers');
my($fail, @containers) = get_containers();
my($stat_fail, %stats) = get_stats();

if ($fail) {
    print ui_alert_box($fail, 'danger');
} else {
    print ui_columns_start([$text{'label_name'}, $text{'label_label'}, $text{'label_runningfor'}, $text{'label_cpu'}, $text{'label_mem'}, ' ' ]);
    foreach my $u (@containers) {
        print ui_columns_row([
            html_escape($u->{'name'}),
            html_escape($u->{'image'}),
            html_escape($u->{'status'}),
            html_escape($stats{$u->{'id'}}{'cpu'}),
            html_escape($stats{$u->{'id'}}{'memUsage'}) . " (" . html_escape($stats{$u->{'id'}}{'mem'}) . ")",
            sprintf("<a href='command.cgi?c=start&container=%s'>%s</a>", urlize($u->{'name'}), $text{'command_start'}),
            sprintf("<a href='command.cgi?c=stop&container=%s'>%s</a>", urlize($u->{'name'}), $text{'command_stop'}),
            sprintf("<a href='command.cgi?c=restart&container=%s'>%s</a>", urlize($u->{'name'}), $text{'command_restart'}),
        ]);
    }
    print ui_columns_end();
}
print ui_tabs_end_tab('mode', 'containers');

print ui_tabs_end();

ui_print_footer("/", $text{'index'});