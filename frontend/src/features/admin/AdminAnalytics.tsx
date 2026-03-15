import React, { useState, useEffect } from 'react';
import {
    VStack, Heading, Text, SimpleGrid, Box, Badge, 
    Icon, Skeleton, HStack, Center, Grid, GridItem, Stack
} from '@chakra-ui/react';
import { TrendingUp, ArrowUpRight, Info } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

export default function AdminAnalytics() {
    const [analysis, setAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`${API_BASE}/admin/financial/predictive`)
            .then(res => setAnalysis(res.data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    const hasData = analysis && analysis.insights?.length > 0;

    const GlassCard = ({ children, ...props }: any) => (
        <Box bg="white" borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100" p={6} {...props}>
            {children}
        </Box>
    );

    return (
        <VStack align="stretch" spacing={8}>
            <Heading size="md">Financial Brain & Analytics</Heading>
            
            {loading ? (
                <Skeleton height="300px" borderRadius="2xl" />
            ) : hasData ? (
                <Grid templateColumns={{ base: "1fr", md: "2fr 1fr" }} gap={8}>
                    <GridItem>
                        <GlassCard border="2px solid" borderColor="pink.100" bg="pink.50">
                            <Heading size="sm" mb={4} color="pink.700"><Icon as={TrendingUp} mr={2} /> Insights Bella IA</Heading>
                            <Stack spacing={3}>
                                {analysis.insights.map((ins: string, i: number) => (
                                    <HStack key={i} p={3} bg="white" borderRadius="lg">
                                        <Icon as={ArrowUpRight} color="pink.500" />
                                        <Text fontWeight="600" fontSize="sm">{ins}</Text>
                                    </HStack>
                                ))}
                            </Stack>
                        </GlassCard>
                    </GridItem>
                    <GridItem>
                        <GlassCard>
                            <Heading size="xs" mb={4} textTransform="uppercase">Top Performers</Heading>
                            <Stack spacing={3}>
                                {analysis.top_performers?.map((n: string, i: number) => (
                                    <HStack key={i} justify="space-between">
                                        <Text fontWeight="bold" fontSize="sm">{n}</Text>
                                        <Badge colorScheme="blue">TOP {i + 1}</Badge>
                                    </HStack>
                                ))}
                            </Stack>
                        </GlassCard>
                    </GridItem>
                </Grid>
            ) : (
                <GlassCard>
                    <Center flexDirection="column" p={10}>
                        <Icon as={Info} w={12} h={12} color="gray.300" mb={4} />
                        <Text color="gray.500">Dados insuficientes para análise preditiva no momento.</Text>
                    </Center>
                </GlassCard>
            )}
        </VStack>
    );
}

